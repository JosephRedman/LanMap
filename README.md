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
- Sucky topology mapping using nmap (When installing check "Support raw 802.11 traffic (and monitor mode)" and "WinPcap API-compatible mode")

## Shortcuts  
- `SHIFT+A`: Add a node to the map.  
- `SHIFT+C`: Edit the color of a selected node or connection.  
- `SHIFT+T`: Add a text label.  
- `SHIFT+H`: Open the Help window.  
- `CTRL+S`: Save the current map.  
- `CTRL+O`: Open a saved map.
- `SHIFT-S`: Map the network topology automatically

## Installation

1. Clone the repository:  
   ```
   git clone https://github.com/JosephRedman/lanmap.git  
   cd lanmap
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

4. Install nmap:
   ```
   https://nmap.org/download.html
   ```
5. Run the application:
   ```
   python Main.py
   ```
   If you have an error along the lines of: `RuntimeError: Sniffing and sending packets is not available at layer 2: winpcap is not installed. You may use conf.L3socket or conf.L3socket6 to access layer 3`, you should (re)install nmap.
   
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
