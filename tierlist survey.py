import tkinter as tk
from tkinter import messagebox, simpledialog

class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pesquisa em Lista de Tiers")
        
        self.items = ["Item 1", "Item 2", "Item 3", "Item 4"]
        self.tiers = ["S", "A", "B", "C", "D"]
        self.current_tier = {item: None for item in self.items}  # Acompanha o tier atual de cada item

        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#f5f5f5")
        self.frames = {}

        # Cria quadros para os tiers
        for idx, tier in enumerate(self.tiers):
            frame = tk.Frame(self.root, bd=2, relief="ridge", bg="#ffffff")
            frame.grid(row=1, column=idx, sticky="nsew", padx=10, pady=10)

            label = tk.Label(frame, text=tier, font=("Arial", 16), bg="#ffffff")
            label.pack(anchor="n", pady=10)
            label.bind("<Button-3>", lambda event, lbl=label: self.rename(event, lbl, "tier"))
            self.frames[tier] = frame

        # Cria etiquetas arrastáveis para os items
        for item in self.items:
            label = tk.Label(self.root, text=item, bg="#e0e0e0", padx=10, pady=5)
            label.grid(row=0, column=self.items.index(item), padx=10, pady=10, sticky="nsew")
            label.bind("<ButtonPress-1>", self.on_drag_start)
            label.bind("<B1-Motion>", self.on_drag_motion)
            label.bind("<ButtonRelease-1>", self.on_drop)
            label.bind("<Button-3>", lambda event, lbl=label: self.rename(event, lbl, "item"))

        # Botão enviar para finalizar a classificação
        tk.Button(self.root, text="Enviar", command=self.submit, bg="#4caf50", fg="white").grid(row=2, columnspan=len(self.tiers), pady=20, padx=10)

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_data = {"x": event.x, "y": event.y}
        widget.configure(bg="#bdbdbd")
        widget.lift()

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_data["x"] + event.x
        y = widget.winfo_y() - widget._drag_data["y"] + event.y
        widget.place(x=x, y=y)

    def on_drop(self, event):
        widget = event.widget
        widget.configure(bg="#e0e0e0")

        for tier, frame in self.frames.items():
            if (widget.winfo_rootx() < frame.winfo_rootx() + frame.winfo_width() and 
                widget.winfo_rootx() + widget.winfo_width() > frame.winfo_rootx() and
                widget.winfo_rooty() < frame.winfo_rooty() + frame.winfo_height() and 
                widget.winfo_rooty() + widget.winfo_height() > frame.winfo_rooty()):
                widget.grid_forget()
                widget.place_forget()
                widget.pack(in_=frame)
                
                # Atualiza o tier atual do item
                self.current_tier[widget.cget("text")] = tier
                break
            else:
                widget.grid()
                # Se o item não estiver em nenhum quadro de tier, atualiza seu tier atual para None
                self.current_tier[widget.cget("text")] = None

    def rename(self, event, widget, type):
        new_name = simpledialog.askstring("Renomear", f"Digite o novo nome para {widget.cget('text')}")
        if new_name:
            if type == "item":
                old_name = widget.cget('text')
                self.items[self.items.index(old_name)] = new_name
                self.current_tier[new_name] = self.current_tier.pop(old_name)
            widget.config(text=new_name)

    def submit(self):
        results = {tier: [] for tier in self.tiers}
        
        for item, tier in self.current_tier.items():
            if tier:
                results[tier].append(item)

        # Formatação dos resultados para exibição
        formatted_results = []
        for tier, items in results.items():
            count = len(items)
            items_str = ', '.join(items) if items else 'Nenhum'
            formatted_results.append(f"{tier} Tier ({count} item(s)): {items_str}")

        messagebox.showinfo("Resultados da Pesquisa", "\n".join(formatted_results))

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()
