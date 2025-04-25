import os
import shutil
import tkinter as tk
from tkinter import messagebox

#
target_folder = os.getcwd()

#ユーザーから拡張子の入力をもらう
ext_to_folder = {
    '.jpg': 'images',
    '.jpeg': 'images',
    '.png': 'images',
    '.pdf': 'pdfs',
    '.mp4': 'videos',
    '.txt': 'text_files',
    '.csv': 'spreadsheets',
    '.py': 'python_files',
}

#対象ファイルを収集
file_list = []
for filename in os.listdir(target_folder):
    file_path = os.path.join(target_folder, filename)
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in ext_to_folder:
            folder_name = ext_to_folder[ext]
            file_list.append((filename, folder_name))
            
#GUI表示
def show_selectable_list():
    root = tk.Tk()
    root.title("整理したいファイルを選んでください")
    root.geometry("400x400")
    
    label = tk.Label(root, text="Ctrl や Shift で複数選択できます")
    label.pack()
    
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for i, (filename, folder) in enumerate(file_list):
        listbox.insert(tk.END, f"{filename} →　{folder}")
    listbox.pack(expand=True, fill="both")
    
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)
    def toggle_select_all():
        if select_all_state["selected"]:
            listbox.select_clear(0, tk.END)
            select_all_state["selected"] = False
        else:
            listbox.select_set(0, tk.END)
            select_all_state["selected"] = True
            
        update_selection_label()    
    
    select_all_btn = tk.Button(top_frame, text="全て選択", width=10, command=toggle_select_all)
    select_all_btn.pack(side="left", padx=5)
    
    
    def move_selected_files():
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("選択なし", "ファイルが選択されてません。 ")
            return
        for index in selected_indices:
            filename, folder_name = file_list[index]
            file_path = os.path.join(target_folder, filename)
            dest_folder = os.path.join(target_folder, folder_name)
            dest_path = os.path.join(dest_folder, filename)
            if os.path.isfile(dest_folder):
                messagebox.showerror("エラー",f"'{dest_folder}' はすでにファイルとして存在しています。整理できません。")
                continue
            
            os.makedirs(dest_folder, exist_ok=True)
            
            base, ext = os.path.splitext(filename)
            dest_path = os.path.join(dest_folder, filename)
            counter= 1
            
            while os.path.exists(dest_path):
                new_name = f"{base}_{counter}{ext}"
                dest_path = os.path.join(dest_folder, new_name)
                counter += 1
                
            shutil.move(file_path, dest_path)
        messagebox.showinfo("完了", "選択したファイルを整理しました!")
        root.destroy()
    
    run_btn = tk.Button(top_frame, text="整理する", width=10, command=move_selected_files)
    run_btn.pack(side="left", padx=5)
    
    selection_label = tk.Label(top_frame, text="選択中: 0 件")
    selection_label.pack(side="right", padx=10)
    
    
    
    
    
    
    
    
    def update_selection_label(event=None):
        selected = listbox.curselection()
        total = listbox.size()
        count = len(selected)
        
        selection_label.config(text=f"選択中: {count} 件")
        
        if count == total and total != 0:
            select_all_btn.config(text="全て解除")
            select_all_state["selected"] = True
        else:
            select_all_btn.config(text="全て選択")
            select_all_state["selected"] = False
                                  
        
    listbox.bind('<<ListboxSelect>>', update_selection_label)    
    
    select_all_state = {"selected": False}
    
    
    
    
        
    frame = tk.Frame(root)
    frame.pack(pady=5)
        
    
    root.mainloop()
    
show_selectable_list()    