# LanMap  

**LanMap** is a simple network topology editor for creating, editing, and visualizing network diagrams.  

## Features  
- Add nodes (Switch, Computer, Server, or custom types) to the map.  
- Create connections between nodes with a double-click.  
- Drag and drop nodes with connections dynamically updated.  
- Customize colors of nodes and connections using a color palette.  
- Add and edit draggable text labels.  
- Save and open maps using the built-in Windows file selector.  
- View instructions via a dedicated "Help" window (press `SHIFT+H`).  

## Shortcuts  
- `SHIFT+A`: Add a node to the map.  
- `SHIFT+C`: Edit the color of a selected node or connection.  
- `SHIFT+T`: Add a text label.  
- `SHIFT+H`: Open the Help window.  
- `CTRL+S`: Save the current map.  
- `CTRL+O`: Open a saved map.  

## Installation  
1. Clone the repository:  
   ```
   git clone https://github.com/JosephRedman/lanmap.git  
   cd lanmap
   ```

2. Run the application:
   ```
   python Main.py
   ```

## TODO:

- [ ] **Node Features**
      
      - Allow renaming of nodes directly on the canvas.
      
      - Add predefined icons for noed types.
      

- [ ] **Connection Features**
      
      - Add Styles (e.g. dashed or bold) for connections
      
      - Allow labeling of connections.
      

- [ ] **UI Enhancements**
      
      - Add a zoom/pan feature for large diagrams.
      
      - Implement undo/redo functionality.


- [ ] **File Support**
      
      - Add support for exporting maps as an image.
      
      - Enable importing/exporting maps in other formats like XML.


- [ ] **Testing**
      
      - Write unit tests for core functionalities.


## License
This project is licenced under the MIT License.
