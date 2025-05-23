import nuke
import os
import time

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets # Nuke 16+

from nukescripts import executeInMainThreadWithResult


def create_export_review_nc(output_path, slate_image=None, logo_path=None):
    """
    Creates a basic review render setup in Nuke Non-Commercial
    """
    def create(node_type):
        node = nuke.createNode(node_type, inpanel=False)
        if node is None:
            nuke.message(f"Error: Cannot create node '{node_type}' (Non-Commercial limit reached).")
        else:
            nuke.autoplace(node)
        return node

    read = nuke.selectedNode() if nuke.selectedNodes() else nuke.toNode("Read1")
    if not read:
        nuke.message("No input Read node selected.")
        return

    # Burn-in text node
    burnin = create("Text")
    if not burnin:
        return
    burnin.setName("Text_BurnIn")
    burnin["box"].setValue([0, 0, 1920, 100])
    burnin["message"].setValue("[value root.name]  Frame: [frame]")
    burnin["size"].setValue(48)
    burnin.setInput(0, read)

    # Slate background
    if slate_image and os.path.exists(slate_image):
        slate_bg = create("Read")
        if not slate_bg:
            return
        slate_bg["file"].setValue(slate_image)
    else:
        slate_bg = create("Constant")
        if not slate_bg: 
            return
        slate_bg["format"].setValue("HD_1080")
        slate_bg["color"].setValue([0.2, 0.2, 0.2, 1])

    # Slate text
    slate_text = create("Text")
    if not slate_text: 
        return
    slate_text.setName("Slate_Text")
    slate_text["box"].setValue([0, 0, 1920, 150])
    executeInMainThreadWithResult(lambda: time.sleep(0.01))
    if "leading" in slate_text.knobs():
        slate_text["leading"].setValue(0)
        slate_text["xjustify"].setValue("left")
        slate_text["yjustify"].setValue("top")
    slate_text["message"].setValue("SLATE\\n[basename [value root.name]]")
    slate_text["size"].setValue(60)
    slate_text.setInput(0, slate_bg)

    final_slate = slate_text

    # Optional logo in top-right corner
    if logo_path and os.path.exists(logo_path):
        logo = create("Read")
        if not logo:
            return
        logo["file"].setValue(logo_path)

        logo_width = logo.width()
        logo_height = logo.height()

        fmt_w = nuke.root().format().width()
        fmt_h = nuke.root().format().height()

        scale_factor = (fmt_h * 0.1) / logo_height
        scaled_w = logo_width * scale_factor
        scaled_h = logo_height * scale_factor

        translate_x = fmt_w // 2 - scaled_w - -30
        translate_y = fmt_h // 2 - scaled_h - 200

        transform = create("Transform")
        if not transform: 
            return
        transform.setName("Logo_Transform")
        transform["scale"].setValue(scale_factor)
        transform["center"].setValue([0, 0])
        transform["translate"].setValue([translate_x, translate_y])
        transform["filter"].setValue("cubic")
        transform["black_outside"].setValue(True)
        transform.setInput(0, logo)

        merge = create("Merge2")
        if not merge:
            return
        merge.setName("Merge_Logo")
        merge.setInput(0, slate_text)
        merge.setInput(1, transform)

        final_slate = merge

    # AppendClip: combine slate + shot
    append = create("AppendClip")
    if not append: 
        return
    append.setName("Append_Slate_Footage")
    append.setInput(0, final_slate)
    append.setInput(1, burnin)

    # Final Write node
    write = create("Write")
    if not write: 
        return
    write.setName("Write_Review")
    write["file"].setValue(output_path)
    write["file_type"].setValue("mov")
    write["meta_codec"].setValue("libx264")
    write["fps"].setValue(nuke.root()["fps"].value())
    write.setInput(0, append)

    print(f"Review export created: {output_path}")


class ExportReviewUI(QtWidgets.QDialog):
    """
    trigger the review export creation.
    """

    def __init__(self):
        super(ExportReviewUI, self).__init__()
        self.setWindowTitle("Auto Review Export")
        self.setMinimumWidth(400)
        layout = QtWidgets.QVBoxLayout()

        # Output path
        layout.addWidget(QtWidgets.QLabel("Output path (.mov):"))
        self.output_line = QtWidgets.QLineEdit()
        browse_out = QtWidgets.QPushButton("Browse")
        browse_out.clicked.connect(self.select_output)
        out_layout = QtWidgets.QHBoxLayout()
        out_layout.addWidget(self.output_line)
        out_layout.addWidget(browse_out)
        layout.addLayout(out_layout)

        # Logo
        layout.addWidget(QtWidgets.QLabel("Optional logo image:"))
        self.logo_line = QtWidgets.QLineEdit()
        browse_logo = QtWidgets.QPushButton("Browse")
        browse_logo.clicked.connect(self.select_logo)
        logo_layout = QtWidgets.QHBoxLayout()
        logo_layout.addWidget(self.logo_line)
        logo_layout.addWidget(browse_logo)
        layout.addLayout(logo_layout)

        # Slate image
        layout.addWidget(QtWidgets.QLabel("Optional slate background image:"))
        self.slate_line = QtWidgets.QLineEdit()
        browse_slate = QtWidgets.QPushButton("Browse")
        browse_slate.clicked.connect(self.select_slate)
        slate_layout = QtWidgets.QHBoxLayout()
        slate_layout.addWidget(self.slate_line)
        slate_layout.addWidget(browse_slate)
        layout.addLayout(slate_layout)

        # Export button
        export_btn = QtWidgets.QPushButton("Create Export")
        export_btn.clicked.connect(self.export)
        layout.addWidget(export_btn)

        self.setLayout(layout)

    def select_output(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Select Output File", "", "QuickTime (*.mov)")
        if path:
            self.output_line.setText(path)

    def select_logo(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Logo Image", "", "Images (*.png *.jpg *.exr)")
        if path:
            self.logo_line.setText(path)

    def select_slate(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Slate Image", "", "Images (*.png *.jpg *.exr)")
        if path:
            self.slate_line.setText(path)

    def export(self):
        output = self.output_line.text().strip()
        logo = self.logo_line.text().strip() or None
        slate = self.slate_line.text().strip() or None
        if not output:
            nuke.message("Please select an output file.")
            return
        create_export_review_nc(output, slate_image=slate, logo_path=logo)
        self.close()


def show_export_ui_nc():
    """
    Launches the UI
    """
    global export_ui_nc
    try:
        export_ui_nc.close()
    except:
        pass
    export_ui_nc = ExportReviewUI()
    export_ui_nc.show()
