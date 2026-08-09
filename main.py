import os
import tkinter as tk
from tkinter import filedialog, messagebox

from pypdf import PdfWriter


class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("620x420")
        self.selected_files = []

        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Selected PDF files:", font=(None, 11, "bold")).pack(anchor="w")

        self.file_listbox = tk.Listbox(frame, selectmode=tk.EXTENDED, height=14)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=(6, 10))

        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Add PDFs", command=self.add_files, width=12).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_selected, width=15).pack(side=tk.LEFT, padx=6)
        tk.Button(button_frame, text="Clear List", command=self.clear_list, width=12).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Merge PDFs", command=self.merge_files, width=12).pack(side=tk.RIGHT)

        self.status_label = tk.Label(self, text="Pick two or more PDF files to merge.", anchor="w")
        self.status_label.pack(fill=tk.X, padx=12, pady=(8, 10))

    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file_paths:
            return

        for file_path in file_paths:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self.file_listbox.insert(tk.END, os.path.basename(file_path))

        self.status_label.config(text=f"{len(self.selected_files)} file(s) selected.")

    def remove_selected(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            messagebox.showinfo("Remove PDF", "Select one or more files to remove.")
            return

        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.selected_files[index]

        self.status_label.config(text=f"{len(self.selected_files)} file(s) selected.")

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)
        self.selected_files.clear()
        self.status_label.config(text="Pick two or more PDF files to merge.")

    def merge_files(self):
        if len(self.selected_files) < 2:
            messagebox.showwarning("Merge PDFs", "Select at least two PDF files to merge.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf",
            title="Save merged PDF as",
        )
        if not output_path:
            return

        try:
            writer = PdfWriter()
            for pdf_path in self.selected_files:
                writer.append(pdf_path)
            with open(output_path, "wb") as out_file:
                writer.write(out_file)

            messagebox.showinfo("Merge Successful", f"Merged PDF saved to:\n{output_path}")
            self.status_label.config(text=f"Merged {len(self.selected_files)} files successfully.")
        except Exception as exc:
            messagebox.showerror("Merge Failed", f"Unable to merge PDFs:\n{exc}")
            self.status_label.config(text="Merge failed. Check file paths and try again.")


if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()