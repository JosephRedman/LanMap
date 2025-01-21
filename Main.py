import json
import tkinter as tk
from tkinter import simpledialog, colorchooser, filedialog

Version = "0.1.5"
Contributers = "Joseph Redman"
class LanMap:
    def __init__(self, root):
        self.root = root
        self.root.title("LanMap v" + Version)
        
        self.canvas = tk.Canvas(root, bg="white", width=1600, height=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.nodes = {}  # Store nodes and their properties
        self.connections = []  # Store connections between nodes
        self.labels = []  # Store labels
        self.dragging_node = None
        self.node_id_counter = 1
        self.selected_node = None
        self.selected_connection = None
        self.selected_label = None

        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Double-1>", self.on_double_click)
        self.root.bind("<Shift-A>", self.open_add_menu)
        self.root.bind("<Shift-C>", self.open_color_palette)
        self.root.bind("<Shift-T>", self.add_label)
        self.root.bind("<Control-s>", lambda e: self.save_map())
        self.root.bind("<Control-o>", lambda e: self.load_map())
        self.root.bind("<Shift-H>", self.open_help_window)



        # Add text elements with placeholders
        self.instruction_text_1 = self.canvas.create_text(0, 0, text="Press 'SHIFT+H' to get help.", anchor="nw")
        self.version_text = self.canvas.create_text(0, 0, text=f"LANMAP v{Version} by {Contributers}.", anchor="sw")

        # Bind to resize event
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update positions relative to canvas size
        self.canvas.coords(self.instruction_text_1, 10, 10)
        self.canvas.coords(self.version_text, 10, event.height - 10)

    

    def on_canvas_click(self, event):
        # Reset selections
        self.selected_node = None
        self.selected_connection = None
        self.selected_label = None

        # Check if clicking on a node
        clicked_item = self.canvas.find_closest(event.x, event.y)
        for node_id, properties in self.nodes.items():
            if clicked_item[0] in (properties["node"], properties["text"]):
                self.dragging_node = node_id
                self.selected_node = node_id
                return

        # Check if clicking on a connection
        for conn in self.connections:
            if clicked_item[0] == conn[2]:
                self.selected_connection = conn[2]
                # Highlight the connection
                self.canvas.itemconfig(conn[2], width=2)
                return

        # Check if clicking on a label
        for label in self.labels:
            if clicked_item[0] == label:
                self.selected_label = label
                return


    def open_add_menu(self, event=None):
        add_menu = tk.Toplevel(self.root)
        add_menu.title("Add Node Menu")
        add_menu.geometry("300x200")

        def add_node_type(node_type):
            self.add_node(node_type, 100, 100)
            add_menu.destroy()

        tk.Button(add_menu, text="Switch", command=lambda: add_node_type("Switch"), width=15).pack(pady=5)
        tk.Button(add_menu, text="Computer", command=lambda: add_node_type("Computer"), width=15).pack(pady=5)
        tk.Button(add_menu, text="Server", command=lambda: add_node_type("Server"), width=15).pack(pady=5)

        custom_frame = tk.Frame(add_menu)
        custom_frame.pack(pady=10)
        tk.Label(custom_frame, text="Custom:").pack(side=tk.LEFT, padx=5)
        custom_entry = tk.Entry(custom_frame)
        custom_entry.pack(side=tk.LEFT, padx=5)

        def add_custom_node():
            custom_type = custom_entry.get().strip()
            if custom_type:
                self.add_node(custom_type, 100, 100)
                add_menu.destroy()

        tk.Button(add_menu, text="Add Custom", command=add_custom_node, width=15).pack(pady=5)

    def open_help_window(self, event=None):
        # Create a new window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("400x300")

        # Instructions text
        instructions = [
            "Press 'SHIFT+A' to add a node to the map.",
            "Press 'SHIFT+C' to edit the color of a node or connection.",
            "Press 'SHIFT+T' to add a text label.",
            "Double-click on 2 nodes to make a connection.",
            "Press 'SHIFT+H' to view this help menu.",
            "Use 'CTRL+S' to save the map and 'CTRL+O' to open a saved map.",
        ]

        # Display the instructions
        for instruction in instructions:
            tk.Label(help_window, text=instruction, anchor="w", justify="left").pack(padx=10, pady=5, anchor="w")

        # Add a close button
        tk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)

    def save_map(self):
        filename = filedialog.asksaveasfilename(
            title="Save Map",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:  # User canceled
            return

        data = {
            "nodes": [
                {
                    "id": node_id,
                    "type": props["type"],
                    "x": props["x"],
                    "y": props["y"],
                    "color": self.canvas.itemcget(props["node"], "fill"),
                }
                for node_id, props in self.nodes.items()
            ],
            "connections": [
                {
                    "start_node": conn[0],
                    "end_node": conn[1],
                    "color": self.canvas.itemcget(conn[2], "fill"),
                }
                for conn in self.connections
            ],
            "labels": [
                {
                    "x": self.canvas.coords(label)[0],
                    "y": self.canvas.coords(label)[1],
                    "text": self.canvas.itemcget(label, "text"),
                }
                for label in self.labels
            ],
        }

        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Map saved to {filename}")
        except Exception as e:
            print(f"Error saving map: {e}")


    def load_map(self):
        filename = filedialog.askopenfilename(
            title="Open Map",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:  # User canceled
            return

        try:
            with open(filename, "r") as file:
                data = json.load(file)

            # Clear current map
            for node_id, props in self.nodes.items():
                self.canvas.delete(props["node"])
                self.canvas.delete(props["text"])
            for conn in self.connections:
                self.canvas.delete(conn[2])
            for label in self.labels:
                self.canvas.delete(label)

            self.nodes.clear()
            self.connections.clear()
            self.labels.clear()
            self.node_id_counter = 1

            # Load nodes
            for node in data["nodes"]:
                self.add_node(node["type"], node["x"], node["y"])
                self.canvas.itemconfig(self.nodes[self.node_id_counter - 1]["node"], fill=node["color"])

            # Load connections
            for conn in data["connections"]:
                self.create_connection(conn["start_node"], conn["end_node"])
                self.canvas.itemconfig(self.connections[-1][2], fill=conn["color"])

            # Load labels
            for label in data["labels"]:
                label_id = self.canvas.create_text(
                    label["x"], label["y"], text=label["text"], font=("Arial", 12), fill="black", tags="label"
                )
                self.labels.append(label_id)

            print(f"Map loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found!")
        except json.JSONDecodeError:
            print(f"Error decoding {filename}")
        except Exception as e:
            print(f"Error loading map: {e}")



    def open_color_palette(self, event=None):
        if self.selected_node:
            color = colorchooser.askcolor(title="Choose Node Color")[1]
            if color:
                self.canvas.itemconfig(self.nodes[self.selected_node]["node"], fill=color)
        elif self.selected_connection:
            color = colorchooser.askcolor(title="Choose Connection Color")[1]
            if color:
                self.canvas.itemconfig(self.selected_connection, fill=color)

    def add_label(self, event=None):
        label_text = simpledialog.askstring("Add Label", "Enter label text:")
        if label_text:
            x, y = 100, 100  # Default position for the label
            label = self.canvas.create_text(x, y, text=label_text, font=("Arial", 12), fill="black", tags="label")
            self.labels.append(label)

            def on_label_click(event, label=label):
                if self.selected_label == label:
                    new_text = simpledialog.askstring("Edit Label", "Edit label text:", initialvalue=self.canvas.itemcget(label, "text"))
                    if new_text:
                        self.canvas.itemconfig(label, text=new_text)
                self.selected_label = label

            self.canvas.tag_bind(label, "<Button-1>", on_label_click)

            # Allow label dragging
            def on_label_drag(event, label=label):
                self.canvas.coords(label, event.x, event.y)

            self.canvas.tag_bind(label, "<B1-Motion>", on_label_drag)

    def add_node(self, node_type, x, y):
        node_id = self.node_id_counter
        self.node_id_counter += 1

        color = "blue" if node_type == "Switch" else "green" if node_type == "Computer" else "purple" if node_type == "Server" else "yellow"
        
        # Draw the circle above the lines
        node = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=f"node{node_id}")
        
        # Draw the text 30px higher than the circle
        text = self.canvas.create_text(x, y-30, text=f"{node_type} {node_id}", tags=f"node{node_id}")

        self.nodes[node_id] = {
            "type": node_type,
            "node": node,
            "text": text,
            "x": x,
            "y": y,
            "highlighted": False
        }

        # Bring the circle and text to the top
        self.canvas.tag_raise(node)
        self.canvas.tag_raise(text)

    def on_canvas_click(self, event):
        # Reset selections
        self.selected_node = None
        self.selected_connection = None
        self.selected_label = None

        # Check if clicking on a node
        clicked_item = self.canvas.find_closest(event.x, event.y)
        for node_id, properties in self.nodes.items():
            if clicked_item[0] in (properties["node"], properties["text"]):
                self.dragging_node = node_id
                self.selected_node = node_id
                return

        # Check if clicking on a connection
        for conn in self.connections:
            if clicked_item[0] == conn[2]:
                self.selected_connection = conn[2]
                # Highlight the connection
                self.canvas.itemconfig(conn[2], width=2)
                return

    def on_canvas_drag(self, event):
        if self.dragging_node:
            # Update node position
            node_id = self.dragging_node
            node = self.nodes[node_id]
            dx, dy = event.x - node["x"], event.y - node["y"]
            
            self.canvas.move(node["node"], dx, dy)
            self.canvas.move(node["text"], dx, dy)
            
            node["x"], node["y"] = event.x, event.y

            # Update connections
            for conn in self.connections:
                if conn[0] == node_id or conn[1] == node_id:
                    start_node = self.nodes[conn[0]]
                    end_node = self.nodes[conn[1]]
                    self.canvas.coords(conn[2], start_node["x"], start_node["y"], end_node["x"], end_node["y"])

    def on_canvas_release(self, event):
        self.dragging_node = None

    def on_double_click(self, event):
        # Highlight node on double-click
        clicked_item = self.canvas.find_closest(event.x, event.y)
        for node_id, properties in self.nodes.items():
            if clicked_item[0] in (properties["node"], properties["text"]):
                self.toggle_highlight(node_id)

                # Check for two highlighted nodes
                highlighted_nodes = [nid for nid, props in self.nodes.items() if props["highlighted"]]
                if len(highlighted_nodes) == 2:
                    self.create_connection(highlighted_nodes[0], highlighted_nodes[1])
                    for nid in highlighted_nodes:
                        self.toggle_highlight(nid)  # Remove highlight after creating connection
                return

    def toggle_highlight(self, node_id):
        node = self.nodes[node_id]
        if node["highlighted"]:
            self.canvas.itemconfig(node["node"], outline="")
        else:
            self.canvas.itemconfig(node["node"], outline="red", width=2)
        node["highlighted"] = not node["highlighted"]

    def create_connection(self, start_node_id, end_node_id):
        # Draw line between nodes
        start_node = self.nodes[start_node_id]
        end_node = self.nodes[end_node_id]
        line = self.canvas.create_line(start_node["x"], start_node["y"], end_node["x"], end_node["y"], fill="black")
        self.connections.append((start_node_id, end_node_id, line))

        # Ensure nodes are above lines
        self.canvas.tag_raise(self.nodes[start_node_id]["node"])
        self.canvas.tag_raise(self.nodes[start_node_id]["text"])
        self.canvas.tag_raise(self.nodes[end_node_id]["node"])
        self.canvas.tag_raise(self.nodes[end_node_id]["text"])

if __name__ == "__main__":
    root = tk.Tk()
    app = LanMap(root)
    root.mainloop()
