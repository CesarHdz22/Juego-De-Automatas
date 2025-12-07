import tkinter as tk
from tkinter import messagebox, simpledialog
from automata.dfa import DFA, State
from engine.level_rules import LEVELS

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego de Autómatas")
        self.state('zoomed')  # ventana maximizada
        self.alphabet = {"a", "b"}
        self.dfa = None
        self.level_idx = 0
        self.state_positions = {}
        self.is_tutorial = False
        self.tutorial_step = 0
        self.state_counter = 0  # nombres automáticos q0, q1...
        self.dragging_state = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.show_menu()

    # ---------------- MENÚ INICIAL ----------------
    def show_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg="#1e1e2f")
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text=" Juego de Autómatas ",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        title.pack(pady=40)

        story = tk.Label(
            frame,
            text=("En el Reino de los Autómatas, los sabios han perdido sus máquinas mágicas.\n"
                  "Tu misión es reconstruirlas paso a paso para restaurar el equilibrio.\n"
                  "Cada nivel te acerca a convertirte en Maestro de Autómatas."),
            font=("Arial", 14),
            fg="white",
            bg="#1e1e2f",
            justify="center"
        )
        story.pack(pady=20)

        tk.Button(frame, text="Iniciar Tutorial", font=("Arial", 18),
                  bg="#4caf50", fg="white", command=self.start_tutorial).pack(pady=20, ipadx=10, ipady=5)
        tk.Button(frame, text="Jugar Niveles", font=("Arial", 18),
                  bg="#2196f3", fg="white", command=self.start_game).pack(pady=20, ipadx=10, ipady=5)
        tk.Button(frame, text="Salir", font=("Arial", 18),
                  bg="#f44336", fg="white", command=self.quit).pack(pady=20, ipadx=10, ipady=5)

    # ---------------- INICIO DE JUEGO ----------------
    def start_game(self):
        self.is_tutorial = False
        self.level_idx = 0
        self.dfa = DFA(alphabet=self.alphabet)
        self.state_positions = {}
        self.state_counter = 0
        self.show_game_ui()

    def start_tutorial(self):
        self.is_tutorial = True
        self.tutorial_step = 0
        self.dfa = DFA(alphabet=self.alphabet)
        self.state_positions = {}
        self.state_counter = 0
        self.show_game_ui()
        messagebox.showinfo("Tutorial", "Bienvenido al tutorial.\nVamos a construir tu primer autómata paso a paso.", parent=self)

    def show_game_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Canvas con borde y espacio
        self.canvas = tk.Canvas(self, bg="#f0f0f0", width=800, height=600,
                                highlightthickness=2, highlightbackground="black")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20, expand=True, fill="both")
        self.canvas.bind("<Double-Button-1>", self.add_state_click)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        # Panel lateral fijo y oscuro
        sidebar = tk.Frame(self, bg="#2c2c3c", width=300)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Estilo de botones
        btn_style = {"font": ("Arial", 14, "bold"), "fg": "white", "width": 20, "height": 2}

        # Botones de interacción
        tk.Button(sidebar, text=" Marcar inicial", bg="#2196f3",
                  command=self.mark_start, **btn_style).pack(pady=6)
        tk.Button(sidebar, text=" Alternar aceptación", bg="#ff9800",
                  command=self.toggle_accept, **btn_style).pack(pady=6)
        tk.Button(sidebar, text=" Agregar transición", bg="#9c27b0",
                  command=self.add_transition, **btn_style).pack(pady=6)
        tk.Button(sidebar, text=" Borrar transición", bg="#e91e63",
                  command=self.delete_transition, **btn_style).pack(pady=6)
        tk.Button(sidebar, text=" Probar nivel", bg="#673ab7",
                  command=self.test_level, **btn_style).pack(pady=10)
        tk.Button(sidebar, text=" Volver al menú", bg="#f44336",
                  command=self.show_menu, **btn_style).pack(pady=10)

        # Campo para simular cadenas
        self.entry = tk.Entry(sidebar, font=("Arial", 12))
        self.entry.pack(pady=4, fill="x")
        tk.Button(sidebar, text="▶ Simular cadena", bg="#607d8b", fg="white",
                  command=lambda: self.simulate(self.entry.get()),
                  font=("Arial", 14, "bold"), width=20, height=2).pack(pady=4)

        # Objetivo destacado
        self.objective_label = tk.Label(sidebar, text="", justify="left", wraplength=260,
                                        bg="#2c2c3c", fg="#ffeb3b", font=("Arial", 12, "bold"))
        self.objective_label.pack(fill="x", pady=6)

        # Descripción y ejemplos
        self.level_label = tk.Label(sidebar, text="", justify="left", wraplength=260,
                                    bg="#2c2c3c", fg="white", font=("Arial", 12))
        self.level_label.pack(fill="x", pady=10)
        self.update_level_text()

        # Texto del paso del tutorial
        self.tutorial_label = tk.Label(sidebar, text="", justify="left", wraplength=260,
                                       bg="#2c2c3c", fg="#ffeb3b", font=("Arial", 12, "bold"))
        self.tutorial_label.pack(fill="x", pady=6)
        self.update_tutorial_text()

    # ---------------- LÓGICA DE JUEGO ----------------
    def update_level_text(self):
        lvl = LEVELS[self.level_idx]
        # Mostrar objetivo si existe; si no, fallback a descripción
        objective_text = getattr(lvl, "objective", lvl.description)
        self.objective_label.config(text=f" Objetivo:\n{objective_text}")
        text = f" Descripción:\n{lvl.description}\n\n"
        text += " Ejemplos aceptados:\n" + "\n".join(getattr(lvl, "examples_pos", [])) + "\n\n"
        text += " Ejemplos rechazados:\n" + "\n".join(getattr(lvl, "examples_neg", []))
        self.level_label.config(text=text)

    def update_tutorial_text(self):
        pasos = [
            "Paso 1: Crea un estado llamado q0.",
            "Paso 2: Marca q0 como estado inicial.",
            "Paso 3: Crea un estado de aceptación llamado q1.",
            "Paso 4: Agrega una transición de q0 a q1 con 'a'.",
            "Paso 5: Haz clic en 'Probar nivel'."
        ]
        if self.is_tutorial and self.tutorial_step < len(pasos):
            self.tutorial_label.config(text=pasos[self.tutorial_step])
        else:
            self.tutorial_label.config(text="")

    def add_state_click(self, event):
        name = f"q{self.state_counter}"
        self.state_counter += 1
        s = self.dfa.add_state(name)
        self.state_positions[s] = (event.x, event.y)
        self.draw_state(s, highlight=True)
        self.after(300, self.redraw)  # vuelve al color normal después de 300ms
        if self.is_tutorial and self.tutorial_step == 0 and name == "q0":
            self.tutorial_step += 1
            messagebox.showinfo("Tutorial", "Ahora marca q0 como estado inicial.", parent=self)
            self.update_tutorial_text()

    def draw_state(self, state: State, highlight=False):
        x, y = self.state_positions[state]
        r = 25
        outline = "green" if state == self.dfa.start else "black"
        fill_color = "yellow" if highlight else "white"
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline=outline, width=2)
        if state in self.dfa.accept:
            self.canvas.create_oval(x - r - 5, y - r - 5, x + r + 5, y + r + 5, outline="blue", width=2)
        self.canvas.create_text(x, y, text=state.name)

    def mark_start(self):
        if not self.dfa.states:
            return
        names = [s.name for s in self.dfa.states]
        name = simpledialog.askstring("Inicial", f"Selecciona estado ({', '.join(names)}):", parent=self)
        if not name:
            return
        st = next((s for s in self.dfa.states if s.name == name), None)
        if not st:
            return
        self.dfa.start = st
        messagebox.showinfo("Listo", f"Estado inicial: {st.name}", parent=self)
        self.redraw()
        if self.is_tutorial and self.tutorial_step == 1 and name == "q0":
            self.tutorial_step += 1
            messagebox.showinfo("Tutorial", "Ahora agrega un estado de aceptación llamado q1.", parent=self)
            self.update_tutorial_text()

    def toggle_accept(self):
        if not self.dfa.states:
            return
        names = [s.name for s in self.dfa.states]
        name = simpledialog.askstring("Aceptar", f"Selecciona estado ({', '.join(names)}):", parent=self)
        if not name:
            return
        st = next((s for s in self.dfa.states if s.name == name), None)
        if not st:
            return
        if st in self.dfa.accept:
            self.dfa.accept.remove(st)
        else:
            self.dfa.accept.add(st)
        self.redraw()
        if self.is_tutorial and self.tutorial_step == 2 and name == "q1":
            self.tutorial_step += 1
            messagebox.showinfo("Tutorial", "Muy bien. Ahora agrega una transición de q0 a q1 con 'a'.", parent=self)
            self.update_tutorial_text()

    def add_transition(self):
        if not self.dfa.states:
            return
        names = [s.name for s in self.dfa.states]
        from_name = simpledialog.askstring("Origen", f"Estado origen ({', '.join(names)}):", parent=self)
        to_name = simpledialog.askstring("Destino", f"Estado destino ({', '.join(names)}):", parent=self)
        symbol = simpledialog.askstring("Símbolo", f"Símbolo ({', '.join(self.alphabet)}):", parent=self)
        if not from_name or not to_name or not symbol:
            return
        st_from = next((s for s in self.dfa.states if s.name == from_name), None)
        st_to = next((s for s in self.dfa.states if s.name == to_name), None)
        if not st_from or not st_to:
            return
        self.dfa.set_transition(st_from, symbol, st_to)
        x1, y1 = self.state_positions[st_from]
        x2, y2 = self.state_positions[st_to]
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2 - 10, text=symbol)
        if self.is_tutorial and self.tutorial_step == 3 and from_name == "q0" and to_name == "q1" and symbol == "a":
            self.tutorial_step += 1
            messagebox.showinfo("Tutorial", "Perfecto. Ahora haz clic en 'Probar nivel'.", parent=self)
            self.update_tutorial_text()

    def redraw(self):
        self.canvas.delete("all")
        for st in self.dfa.states:
            self.draw_state(st)
        for (frm, sym), to in self.dfa.transitions.items():
            x1, y1 = self.state_positions[frm]
            x2, y2 = self.state_positions[to]
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2 - 10, text=sym)

    def simulate(self, cadena):
        if not self.dfa or not self.dfa.start:
            messagebox.showwarning("Error", "Debes marcar un estado inicial antes de simular.", parent=self)
            return
        current = self.dfa.start
        for symbol in cadena:
            # Resaltar estado actual
            x, y = self.state_positions[current]
            r = 25
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="red", width=3)
            self.update()
            self.after(350)  # pausa para animación
            current = self.dfa.transitions.get((current, symbol), None)
            if not current:
                break
        if current and current in self.dfa.accept:
            messagebox.showinfo("Resultado", f"La cadena '{cadena}' es aceptada ✅", parent=self)
        else:
            messagebox.showinfo("Resultado", f"La cadena '{cadena}' es rechazada ❌", parent=self)
        self.redraw()

    def test_level(self):
        if not self.dfa.start:
            messagebox.showwarning("Error", "Debes marcar un estado inicial antes de probar el nivel.", parent=self)
            return

        lvl = LEVELS[self.level_idx]
        ok, msgs = lvl.validator(self.dfa)
        if ok:
            messagebox.showinfo("¡Correcto!", "Objetivo cumplido. Avanzas al siguiente nivel.", parent=self)
            self.level_idx = min(self.level_idx + 1, len(LEVELS) - 1)
            self.update_level_text()
        else:
            messagebox.showwarning("Revisar", "\n".join(msgs), parent=self)

        if self.is_tutorial and self.tutorial_step == 4:
            messagebox.showinfo("Tutorial", "¡Has completado el tutorial!", parent=self)
            self.is_tutorial = False
            self.update_tutorial_text()
    def get_state_at_position(self, x, y):
        for st, (sx, sy) in self.state_positions.items():
            if (x - sx)**2 + (y - sy)**2 <= 25**2:  # radio 25
                return st
        return None
    
    def start_drag(self, event):
        st = self.get_state_at_position(event.x, event.y)
        if st:
            self.dragging_state = st
            sx, sy = self.state_positions[st]
            self.drag_offset_x = sx - event.x
            self.drag_offset_y = sy - event.y

    def do_drag(self, event):
        if self.dragging_state:
            new_x = event.x + self.drag_offset_x
            new_y = event.y + self.drag_offset_y
            self.state_positions[self.dragging_state] = (new_x, new_y)
            self.redraw()
    
    def stop_drag(self, event):
        self.dragging_state = None
    
    def delete_transition(self):
        if not self.dfa.states:
            return

        names = [s.name for s in self.dfa.states]
        from_name = simpledialog.askstring("Origen", f"Estado origen ({', '.join(names)}):", parent=self)
        to_name = simpledialog.askstring("Destino", f"Estado destino ({', '.join(names)}):", parent=self)
        symbol = simpledialog.askstring("Símbolo", f"Símbolo ({', '.join(self.alphabet)}):", parent=self)

        if not from_name or not to_name or not symbol:
            return

        st_from = next((s for s in self.dfa.states if s.name == from_name), None)
        st_to = next((s for s in self.dfa.states if s.name == to_name), None)

        if not st_from or not st_to:
            messagebox.showwarning("Error", "Estado no encontrado.", parent=self)
            return

        key = (st_from, symbol)

        if key in self.dfa.transitions and self.dfa.transitions[key] == st_to:
            del self.dfa.transitions[key]
            messagebox.showinfo("Listo", "Transición eliminada.", parent=self)
            self.redraw()
        else:
            messagebox.showwarning("Error", "Esa transición no existe.", parent=self)

def run_app():
    app = App()
    app.mainloop()