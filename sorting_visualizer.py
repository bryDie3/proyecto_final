"""
Visualizador de Estructuras de Datos
- Lista Simple (Single Linked List)
- Lista Doble (Doubly Linked List)
- Árbol Binario con BFS (Binary Search Tree + BFS)
UI con Tkinter - diseño oscuro industrial
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import time
import math


# ─────────────────────────────────────────────
#  ESTRUCTURAS DE DATOS
# ─────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class SingleLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def delete(self, data):
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            return True
        cur = self.head
        while cur.next:
            if cur.next.data == data:
                cur.next = cur.next.next
                return True
            cur = cur.next
        return False

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node
        new_node.prev = cur

    def delete(self, data):
        cur = self.head
        while cur:
            if cur.data == data:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                return True
            cur = cur.next
        return False

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        if data < node.data:
            if node.left:
                self._insert(node.left, data)
            else:
                node.left = TreeNode(data)
        else:
            if node.right:
                self._insert(node.right, data)
            else:
                node.right = TreeNode(data)

    def delete(self, data):
        self.root, deleted = self._delete(self.root, data)
        return deleted

    def _delete(self, node, data):
        if not node:
            return node, False
        if data < node.data:
            node.left, deleted = self._delete(node.left, data)
        elif data > node.data:
            node.right, deleted = self._delete(node.right, data)
        else:
            if not node.left:
                return node.right, True
            if not node.right:
                return node.left, True
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            node.data = min_node.data
            node.right, _ = self._delete(node.right, min_node.data)
            deleted = True
        return node, deleted

    def bfs(self):
        """Retorna lista de niveles (list of lists) para visualización."""
        if not self.root:
            return []
        levels, queue = [], [self.root]
        while queue:
            level, next_q = [], []
            for n in queue:
                level.append(n.data if n else None)
                if n:
                    next_q.append(n.left)
                    next_q.append(n.right)
            levels.append(level)
            queue = [n for n in next_q if n]
        return levels


# ─────────────────────────────────────────────
#  COLORES Y TEMA
# ─────────────────────────────────────────────

BG       = "#0e0f13"
PANEL    = "#16171d"
CARD     = "#1e2029"
ACCENT   = "#f0c040"
ACCENT2  = "#4fc3f7"
ACCENT3  = "#ef5350"
TEXT     = "#e8e8e8"
MUTED    = "#6b7280"
BORDER   = "#2a2d3a"
NODE_C   = "#f0c040"
NODE_TXT = "#0e0f13"
ARROW    = "#4fc3f7"
PREV_C   = "#ef5350"


# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estructuras de Datos — Visualizador")
        self.geometry("1200x780")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.sll  = SingleLinkedList()
        self.dll  = DoublyLinkedList()
        self.bst  = BinarySearchTree()

        self._build_fonts()
        self._build_ui()

    def _build_fonts(self):
        self.f_title  = font.Font(family="Courier New", size=14, weight="bold")
        self.f_label  = font.Font(family="Courier New", size=10)
        self.f_small  = font.Font(family="Courier New", size=9)
        self.f_node   = font.Font(family="Courier New", size=11, weight="bold")
        self.f_header = font.Font(family="Courier New", size=18, weight="bold")

    # ── Layout principal ──────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(18, 0))
        tk.Label(hdr, text="[ DATA STRUCTURES VISUALIZER ]",
                 font=self.f_header, fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text="v1.0", font=self.f_small, fg=MUTED, bg=BG).pack(side="right", pady=8)

        sep = tk.Frame(self, bg=ACCENT, height=2)
        sep.pack(fill="x", padx=20, pady=(6, 14))

        # Notebook (pestañas)
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook",        background=BG,    borderwidth=0)
        style.configure("TNotebook.Tab",    background=PANEL, foreground=MUTED,
                        font=("Courier New", 10, "bold"),
                        padding=[16, 8], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self._tab_sll  = self._make_tab(nb, "Lista Simple",  self.sll,  "sll")
        self._tab_dll  = self._make_tab(nb, "Lista Doble",   self.dll,  "dll")
        self._tab_bst  = self._make_tab_bst(nb)
        self._tab_help = self._make_tab_help(nb)

        nb.add(self._tab_sll,  text="  ◈ Lista Simple  ")
        nb.add(self._tab_dll,  text="  ◈ Lista Doble   ")
        nb.add(self._tab_bst,  text="  ◈ BFS / BST     ")
        nb.add(self._tab_help, text="  ◈ ? Ayuda        ")

    # ── Pestaña genérica SLL / DLL ────────────
    def _make_tab(self, nb, title, structure, tag):
        frame = tk.Frame(nb, bg=CARD)

        # Panel de control
        ctrl = tk.Frame(frame, bg=PANEL, bd=0)
        ctrl.pack(fill="x", padx=16, pady=14)

        tk.Label(ctrl, text=f"DATO:", font=self.f_label, fg=MUTED, bg=PANEL).pack(side="left", padx=(12, 4))
        entry = tk.Entry(ctrl, width=14, font=self.f_label,
                         bg=BG, fg=TEXT, insertbackground=ACCENT,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
        entry.pack(side="left", padx=(0, 10), ipady=5)

        def insert_cmd():
            val = entry.get().strip()
            if not val:
                return
            try:
                val = int(val)
            except ValueError:
                pass
            structure.insert(val)
            entry.delete(0, "end")
            self._redraw(canvas, structure, tag)

        def delete_cmd():
            val = entry.get().strip()
            if not val:
                return
            try:
                val = int(val)
            except ValueError:
                pass
            ok = structure.delete(val)
            entry.delete(0, "end")
            if ok:
                self._redraw(canvas, structure, tag)
            else:
                messagebox.showwarning("No encontrado", f"'{val}' no existe en la lista.")

        def clear_cmd():
            if tag == "sll":
                self.sll = SingleLinkedList()
                structure.__dict__.update(self.sll.__dict__)
            else:
                self.dll = DoublyLinkedList()
                structure.__dict__.update(self.dll.__dict__)
            self._redraw(canvas, structure, tag)

        btn_style = dict(font=self.f_label, relief="flat", cursor="hand2",
                         padx=14, pady=5, bd=0)
        tk.Button(ctrl, text="▶ INSERTAR", bg=ACCENT, fg=NODE_TXT,
                  command=insert_cmd, **btn_style).pack(side="left", padx=4)
        tk.Button(ctrl, text="✕ ELIMINAR", bg=ACCENT3, fg=TEXT,
                  command=delete_cmd, **btn_style).pack(side="left", padx=4)
        tk.Button(ctrl, text="⟳ LIMPIAR", bg=BORDER, fg=MUTED,
                  command=clear_cmd, **btn_style).pack(side="left", padx=4)

        entry.bind("<Return>", lambda e: insert_cmd())

        # Canvas
        canvas = tk.Canvas(frame, bg=CARD, bd=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Leyenda
        self._legend(frame, tag)

        setattr(self, f"_{tag}_entry",  entry)
        setattr(self, f"_{tag}_canvas", canvas)
        setattr(self, f"_{tag}_struct", structure)
        return frame

    def _legend(self, parent, tag):
        leg = tk.Frame(parent, bg=PANEL)
        leg.pack(fill="x", padx=16, pady=(0, 10))
        items = [("●", ACCENT, "Nodo"),
                 ("→", ARROW,  "Siguiente")]
        if tag == "dll":
            items.append(("←", PREV_C, "Anterior"))
        for sym, col, lbl in items:
            tk.Label(leg, text=sym, font=self.f_label, fg=col, bg=PANEL).pack(side="left", padx=(12, 2))
            tk.Label(leg, text=lbl, font=self.f_small, fg=MUTED, bg=PANEL).pack(side="left", padx=(0, 12))

    # ── Pestaña BST + BFS ────────────────────
    def _make_tab_bst(self, nb):
        frame = tk.Frame(nb, bg=CARD)

        ctrl = tk.Frame(frame, bg=PANEL)
        ctrl.pack(fill="x", padx=16, pady=14)

        tk.Label(ctrl, text="DATO:", font=self.f_label, fg=MUTED, bg=PANEL).pack(side="left", padx=(12, 4))
        entry = tk.Entry(ctrl, width=14, font=self.f_label,
                         bg=BG, fg=TEXT, insertbackground=ACCENT,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
        entry.pack(side="left", padx=(0, 10), ipady=5)

        # BFS highlight state
        self._bfs_step   = []
        self._bfs_idx    = 0
        self._bfs_job    = None

        def insert_cmd():
            val = entry.get().strip()
            if not val:
                return
            try:
                val = int(val)
            except ValueError:
                messagebox.showwarning("Error", "Solo se permiten enteros en el BST.")
                return
            self.bst.insert(val)
            entry.delete(0, "end")
            self._redraw_bst()

        def delete_cmd():
            val = entry.get().strip()
            if not val:
                return
            try:
                val = int(val)
            except ValueError:
                return
            ok = self.bst.delete(val)
            entry.delete(0, "end")
            if ok:
                self._redraw_bst()
            else:
                messagebox.showwarning("No encontrado", f"'{val}' no existe en el árbol.")

        def bfs_cmd():
            if not self.bst.root:
                messagebox.showinfo("BFS", "El árbol está vacío.")
                return
            levels = self.bst.bfs()
            flat = [v for lvl in levels for v in lvl]
            self._bfs_step = flat
            self._bfs_idx  = 0
            self._animate_bfs()

        def clear_cmd():
            self.bst = BinarySearchTree()
            self._bfs_step = []
            self._redraw_bst()

        btn_style = dict(font=self.f_label, relief="flat", cursor="hand2",
                         padx=14, pady=5, bd=0)
        tk.Button(ctrl, text="▶ INSERTAR",   bg=ACCENT,  fg=NODE_TXT, command=insert_cmd,  **btn_style).pack(side="left", padx=4)
        tk.Button(ctrl, text="✕ ELIMINAR",   bg=ACCENT3, fg=TEXT,     command=delete_cmd,  **btn_style).pack(side="left", padx=4)
        tk.Button(ctrl, text="⟳ BFS",        bg=ACCENT2, fg=NODE_TXT, command=bfs_cmd,     **btn_style).pack(side="left", padx=4)
        tk.Button(ctrl, text="⟳ LIMPIAR",    bg=BORDER,  fg=MUTED,    command=clear_cmd,   **btn_style).pack(side="left", padx=4)

        entry.bind("<Return>", lambda e: insert_cmd())

        self._bst_canvas = tk.Canvas(frame, bg=CARD, bd=0, highlightthickness=0)
        self._bst_canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Leyenda BFS
        leg = tk.Frame(frame, bg=PANEL)
        leg.pack(fill="x", padx=16, pady=(0, 10))
        for sym, col, lbl in [("●", ACCENT, "Nodo"), ("●", ACCENT2, "BFS activo"), ("→", MUTED, "Rama")]:
            tk.Label(leg, text=sym, font=self.f_label, fg=col, bg=PANEL).pack(side="left", padx=(12, 2))
            tk.Label(leg, text=lbl, font=self.f_small, fg=MUTED, bg=PANEL).pack(side="left", padx=(0, 12))

        return frame

    # ── Pestaña Ayuda / Autoaprendizaje ──────
    def _make_tab_help(self, nb):
        frame = tk.Frame(nb, bg=CARD)

        # ── Banco de preguntas por categoría ──
        QUESTIONS = {
            "📋  Lista Simple": [
                ("¿Qué es un nodo en una lista enlazada?",
                 "Un objeto con dos campos: 'data' (el valor almacenado) y 'next' (puntero al siguiente nodo). El último nodo tiene next = None."),
                ("¿Cuál es la complejidad de insertar al final?",
                 "O(n) porque hay que recorrer toda la lista desde el head hasta encontrar el nodo cuyo next sea None."),
                ("¿Cuál es la complejidad de insertar al inicio?",
                 "O(1). Solo se crea el nuevo nodo, su next apunta al head actual, y head pasa a ser el nuevo nodo."),
                ("¿Qué pasa si pierdes la referencia al head?",
                 "Pierdes acceso a toda la lista. En Python el garbage collector la eliminará, pero en C/C++ ocurre un memory leak."),
                ("¿Cómo detectas un ciclo en una lista enlazada?",
                 "Con el algoritmo de Floyd (dos punteros): un puntero 'lento' avanza 1 paso y uno 'rápido' avanza 2. Si se encuentran, hay ciclo. Complejidad O(n)."),
                ("¿Cómo invertirías una lista enlazada sin usar estructuras extra?",
                 "Con tres punteros: prev=None, cur=head, next_node. En cada iteración: guardar cur.next, apuntar cur.next a prev, mover prev a cur, mover cur a next_node. Al final prev es el nuevo head."),
            ],
            "🔁  Lista Doble": [
                ("¿Qué ventaja tiene la lista doble sobre la simple?",
                 "Permite recorrido en ambas direcciones y eliminación en O(1) si tienes referencia directa al nodo, porque puedes acceder tanto al nodo anterior como al siguiente sin recorrer desde el head."),
                ("¿Cuánta memoria extra consume cada nodo vs la lista simple?",
                 "Un puntero adicional 'prev'. En arquitecturas de 64 bits, eso son 8 bytes extra por nodo."),
                ("¿Cómo eliminas el primer nodo en una lista doble?",
                 "head = head.next. Si el nuevo head no es None, asignar head.prev = None para romper la referencia hacia el nodo eliminado."),
                ("¿Para qué caso de uso usarías una lista doble?",
                 "Historial de navegación (back/forward), implementación de LRU Cache, editores de texto con deshacer/rehacer, o cualquier estructura que necesite navegación bidireccional eficiente."),
                ("¿Qué es un LRU Cache y cómo lo implementarías?",
                 "Least Recently Used Cache. Se implementa con lista doble + hash map. El map guarda referencia directa a cada nodo (O(1) acceso), y la lista mantiene el orden de uso. Al acceder a un elemento se mueve al frente en O(1)."),
            ],
            "🌳  Árbol Binario de Búsqueda (BST)": [
                ("¿Cuál es la propiedad fundamental del BST?",
                 "Todo nodo del subárbol izquierdo es MENOR que el nodo padre, y todo nodo del subárbol derecho es MAYOR O IGUAL. Esto permite búsquedas en O(log n) en un árbol balanceado."),
                ("¿Qué pasa si insertas 1,2,3,4,5 en orden en un BST?",
                 "El árbol degenera en una lista lineal hacia la derecha (como una linked list). Todas las operaciones pasan de O(log n) a O(n). Para evitarlo se usan árboles AVL o Rojo-Negro."),
                ("¿Cómo eliminas un nodo con dos hijos?",
                 "Se busca el sucesor en orden (el menor nodo del subárbol derecho). Se copia su valor al nodo a eliminar, luego se elimina ese sucesor que tiene como máximo un hijo derecho."),
                ("¿Qué es la altura de un árbol y por qué importa?",
                 "Número de aristas en el camino más largo desde la raíz hasta una hoja. Determina la complejidad de búsqueda, inserción y eliminación. Un árbol balanceado tiene altura O(log n)."),
                ("¿Cuál es la altura mínima de un árbol con 14 nodos?",
                 "3 niveles (altura = 3). Un árbol binario completo con altura h tiene como máximo 2^(h+1)-1 nodos. Con h=3: 2^4-1=15 nodos. Con 14 nodos la altura mínima es 3."),
            ],
            "🔍  BFS — Búsqueda por Amplitud": [
                ("¿Qué estructura de datos usa BFS internamente y por qué?",
                 "Una COLA (Queue) — FIFO. Se encola la raíz, luego por cada nodo se procesan todos del nivel actual y se encolan sus hijos. Esto garantiza procesar nivel por nivel de izquierda a derecha."),
                ("¿Cuál es la diferencia entre BFS y DFS?",
                 "BFS recorre nivel por nivel usando una cola — ideal para camino más corto. DFS va hasta el fondo de cada rama usando recursión o pila — ideal para explorar todas las posibilidades. BFS usa más memoria, DFS menos."),
                ("¿Cuál es la complejidad de BFS en tiempo y espacio?",
                 "Tiempo: O(n) — visita cada nodo exactamente una vez. Espacio: O(n) — en el peor caso la cola almacena todos los nodos del último nivel, que en un árbol completo es n/2 nodos."),
                ("¿Para qué sirve BFS en problemas reales?",
                 "Camino más corto en grafos no ponderados, niveles en árboles, flood fill en imágenes, algoritmo de Dijkstra (BFS con prioridad), rastreo de redes sociales por grados de separación."),
                ("¿Qué devuelve BFS nivel por nivel en un BST con 10,5,15,3,7?",
                 "Nivel 0: [10] — Nivel 1: [5, 15] — Nivel 2: [3, 7]. El recorrido BFS completo sería: 10, 5, 15, 3, 7."),
            ],
            "⚡  Complejidades Clave": [
                ("¿Cuál es la tabla de complejidades de las 3 estructuras?",
                 "Lista Simple — Búsqueda: O(n), Inserción inicio: O(1), Inserción fin: O(n), Eliminación: O(n).\nLista Doble — igual pero eliminación con referencia: O(1).\nBST balanceado — Búsqueda: O(log n), Inserción: O(log n), Eliminación: O(log n)."),
                ("¿Cuándo usarías lista enlazada en vez de arreglo?",
                 "Cuando hay muchas inserciones/eliminaciones al inicio o en medio, cuando no conoces el tamaño final, o cuando la memoria está fragmentada. Los arreglos son mejores para acceso aleatorio por índice O(1)."),
                ("¿Qué diferencia hay entre árbol AVL y BST simple?",
                 "El AVL se autobalancea en cada inserción/eliminación usando rotaciones, garantizando altura O(log n) siempre. El BST simple puede degradar a O(n). El AVL tiene operaciones más complejas pero garantiza rendimiento."),
            ],
        }

        # ── Estado de la pregunta actual ──
        self._help_cat_idx = tk.IntVar(value=0)
        self._help_q_idx   = tk.IntVar(value=0)
        self._help_showing = False
        self._help_cats    = list(QUESTIONS.keys())
        self._help_data    = QUESTIONS

        # ── Header ──
        hdr = tk.Frame(frame, bg=PANEL)
        hdr.pack(fill="x", padx=16, pady=14)
        tk.Label(hdr, text="◈ AUTOAPRENDIZAJE — PREGUNTAS DE REPASO",
                 font=self.f_title, fg=ACCENT, bg=PANEL).pack(side="left", padx=12)
        tk.Label(hdr, text="Practica antes de tu examen o entrevista",
                 font=self.f_small, fg=MUTED, bg=PANEL).pack(side="left", padx=8)

        # ── Selector de categoría ──
        cat_frame = tk.Frame(frame, bg=CARD)
        cat_frame.pack(fill="x", padx=16, pady=(0, 6))
        tk.Label(cat_frame, text="CATEGORÍA:", font=self.f_small, fg=MUTED, bg=CARD).pack(side="left", padx=(4, 6))

        self._cat_btns = []
        for i, cat in enumerate(self._help_cats):
            btn = tk.Button(cat_frame, text=cat,
                            font=self.f_small, relief="flat", cursor="hand2",
                            padx=10, pady=4, bd=0,
                            bg=BORDER, fg=MUTED,
                            command=lambda idx=i: self._select_cat(idx))
            btn.pack(side="left", padx=3)
            self._cat_btns.append(btn)

        # ── Tarjeta de pregunta ──
        card = tk.Frame(frame, bg=BG, bd=0)
        card.pack(fill="both", expand=True, padx=16, pady=8)

        # Contador
        self._help_counter = tk.Label(card, text="", font=self.f_small,
                                      fg=MUTED, bg=BG)
        self._help_counter.pack(anchor="ne", padx=16, pady=(12, 0))

        # Pregunta
        q_frame = tk.Frame(card, bg=PANEL, pady=20)
        q_frame.pack(fill="x", padx=12, pady=(4, 0))
        tk.Label(q_frame, text="PREGUNTA", font=self.f_small,
                 fg=ACCENT, bg=PANEL).pack(anchor="w", padx=20)
        self._help_q_lbl = tk.Label(q_frame, text="",
                                     font=self.f_label, fg=TEXT, bg=PANEL,
                                     wraplength=860, justify="left")
        self._help_q_lbl.pack(anchor="w", padx=20, pady=(6, 16))

        # Respuesta (oculta inicialmente)
        a_frame = tk.Frame(card, bg=CARD, pady=16)
        a_frame.pack(fill="x", padx=12, pady=(6, 0))
        tk.Label(a_frame, text="RESPUESTA", font=self.f_small,
                 fg=ACCENT2, bg=CARD).pack(anchor="w", padx=20)
        self._help_a_lbl = tk.Label(a_frame, text="",
                                     font=self.f_label, fg=TEXT, bg=CARD,
                                     wraplength=860, justify="left")
        self._help_a_lbl.pack(anchor="w", padx=20, pady=(6, 16))
        self._help_a_frame = a_frame

        # ── Botones de navegación ──
        nav = tk.Frame(card, bg=BG)
        nav.pack(pady=16)

        btn_s = dict(font=self.f_label, relief="flat", cursor="hand2",
                     padx=18, pady=7, bd=0)

        tk.Button(nav, text="◀ ANTERIOR", bg=BORDER, fg=MUTED,
                  command=self._help_prev, **btn_s).pack(side="left", padx=6)

        self._help_reveal_btn = tk.Button(nav, text="👁  VER RESPUESTA",
                                          bg=ACCENT2, fg=NODE_TXT,
                                          command=self._help_reveal, **btn_s)
        self._help_reveal_btn.pack(side="left", padx=6)

        tk.Button(nav, text="SIGUIENTE ▶", bg=ACCENT, fg=NODE_TXT,
                  command=self._help_next, **btn_s).pack(side="left", padx=6)

        # Barra de progreso
        prog_frame = tk.Frame(card, bg=BG)
        prog_frame.pack(fill="x", padx=12, pady=(4, 0))
        self._prog_bar_bg = tk.Frame(prog_frame, bg=BORDER, height=4)
        self._prog_bar_bg.pack(fill="x", padx=8)
        self._prog_bar    = tk.Frame(self._prog_bar_bg, bg=ACCENT, height=4)
        self._prog_bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

        # Inicializar primera pregunta
        self._select_cat(0)
        return frame

    def _select_cat(self, idx):
        self._help_cat_idx.set(idx)
        self._help_q_idx.set(0)
        self._help_showing = False
        for i, btn in enumerate(self._cat_btns):
            if i == idx:
                btn.configure(bg=ACCENT, fg=NODE_TXT)
            else:
                btn.configure(bg=BORDER, fg=MUTED)
        self._help_load()

    def _help_load(self):
        cat  = self._help_cats[self._help_cat_idx.get()]
        qs   = self._help_data[cat]
        idx  = self._help_q_idx.get()
        q, a = qs[idx]

        self._help_q_lbl.configure(text=q)
        self._help_a_lbl.configure(text="")
        self._help_a_frame.configure(bg=CARD)
        self._help_a_lbl.configure(bg=CARD)
        self._help_showing = False
        self._help_reveal_btn.configure(text="👁  VER RESPUESTA", bg=ACCENT2)
        self._help_counter.configure(text=f"Pregunta {idx+1} / {len(qs)}")

        # Barra de progreso
        rel = (idx + 1) / len(qs)
        self._prog_bar.place(relwidth=rel)

    def _help_reveal(self):
        if self._help_showing:
            return
        cat  = self._help_cats[self._help_cat_idx.get()]
        qs   = self._help_data[cat]
        idx  = self._help_q_idx.get()
        _, a = qs[idx]
        self._help_a_lbl.configure(text=a)
        self._help_showing = True
        self._help_reveal_btn.configure(text="✓ MOSTRADA", bg=BORDER)

    def _help_next(self):
        cat = self._help_cats[self._help_cat_idx.get()]
        qs  = self._help_data[cat]
        idx = self._help_q_idx.get()
        if idx < len(qs) - 1:
            self._help_q_idx.set(idx + 1)
        else:
            self._help_q_idx.set(0)
        self._help_load()

    def _help_prev(self):
        cat = self._help_cats[self._help_cat_idx.get()]
        qs  = self._help_data[cat]
        idx = self._help_q_idx.get()
        if idx > 0:
            self._help_q_idx.set(idx - 1)
        else:
            self._help_q_idx.set(len(qs) - 1)
        self._help_load()

    # ── Dibujo Lista Simple ───────────────────
    def _redraw(self, canvas, structure, tag):
        canvas.delete("all")
        items = structure.to_list()
        if not items:
            canvas.create_text(400, 160, text="[ lista vacía ]",
                               font=self.f_label, fill=MUTED)
            return

        w = canvas.winfo_width() or 900
        r = 28       # radio nodo
        gap = 70     # espacio entre centros
        start_x = 60
        y = 100
        x = start_x

        positions = []
        for i, val in enumerate(items):
            cx = start_x + i * (2 * r + gap)
            positions.append(cx)

        # Dibujar flechas y nodos
        for i, (val, cx) in enumerate(zip(items, positions)):
            # Flecha "next"
            if i < len(items) - 1:
                nx = positions[i + 1]
                ax1, ax2 = cx + r, nx - r
                canvas.create_line(ax1, y, ax2, y, fill=ARROW, width=2, arrow="last",
                                   arrowshape=(10, 12, 4))
                if tag == "dll":
                    canvas.create_line(ax2, y + 12, ax1, y + 12, fill=PREV_C, width=2,
                                       arrow="last", arrowshape=(10, 12, 4))
            else:
                # NULL al final
                ex = cx + r + 30
                canvas.create_line(cx + r, y, ex, y, fill=ARROW, width=2, dash=(4, 4))
                canvas.create_text(ex + 18, y, text="∅", font=self.f_label, fill=MUTED)

            # Nodo
            canvas.create_oval(cx - r, y - r, cx + r, y + r,
                               fill=NODE_C, outline=ACCENT, width=2)
            canvas.create_text(cx, y, text=str(val), font=self.f_node, fill=NODE_TXT)

            # Índice
            canvas.create_text(cx, y + r + 14, text=f"[{i}]",
                               font=self.f_small, fill=MUTED)

        # "Head" label
        canvas.create_text(positions[0], y - r - 18, text="HEAD",
                           font=self.f_small, fill=ACCENT)
        if tag == "dll" and len(positions) > 1:
            canvas.create_text(positions[-1], y - r - 18, text="TAIL",
                               font=self.f_small, fill=PREV_C)

    # ── Dibujo BST ────────────────────────────
    def _redraw_bst(self, highlight=None):
        canvas = self._bst_canvas
        canvas.delete("all")
        if not self.bst.root:
            canvas.create_text(400, 160, text="[ árbol vacío ]",
                               font=self.f_label, fill=MUTED)
            return

        w = canvas.winfo_width() or 900
        h = canvas.winfo_height() or 500

        positions = {}
        self._calc_positions(self.bst.root, 0, w, 60, positions, level=0)
        self._draw_edges(canvas, self.bst.root, positions)
        self._draw_nodes(canvas, positions, highlight)

    def _calc_positions(self, node, lo, hi, y, positions, level):
        if not node:
            return
        mid = (lo + hi) / 2
        positions[id(node)] = (mid, y, node)
        self._calc_positions(node.left,  lo,  mid, y + 80, positions, level + 1)
        self._calc_positions(node.right, mid, hi,  y + 80, positions, level + 1)

    def _draw_edges(self, canvas, node, positions):
        if not node:
            return
        px, py, _ = positions[id(node)]
        for child in (node.left, node.right):
            if child:
                cx, cy, _ = positions[id(child)]
                canvas.create_line(px, py, cx, cy, fill=MUTED, width=1.5)
        self._draw_edges(canvas, node.left,  positions)
        self._draw_edges(canvas, node.right, positions)

    def _draw_nodes(self, canvas, positions, highlight):
        r = 22
        for nid, (x, y, node) in positions.items():
            active = highlight is not None and node.data == highlight
            fill  = ACCENT2 if active else NODE_C
            outline = "#ffffff" if active else ACCENT
            canvas.create_oval(x - r, y - r, x + r, y + r,
                               fill=fill, outline=outline, width=2)
            canvas.create_text(x, y, text=str(node.data),
                               font=self.f_node, fill=NODE_TXT)

    # ── Animación BFS ─────────────────────────
    def _animate_bfs(self):
        if self._bfs_idx >= len(self._bfs_step):
            # fin: redraw sin highlight
            self._redraw_bst(highlight=None)
            return
        val = self._bfs_step[self._bfs_idx]
        self._redraw_bst(highlight=val)
        self._bfs_idx += 1
        self._bfs_job = self.after(600, self._animate_bfs)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    # Forzar redibujado cuando cambia el tamaño
    def on_resize(event):
        try:
            tab = app.nametowidget(app.winfo_children()[-2].select())  # noqa
        except Exception:
            pass
    app.mainloop()