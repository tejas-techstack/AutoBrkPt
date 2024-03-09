from pycfg.pycfg import PyCFG, CFGNode, slurp 
import argparse 
import tkinter as tk 
  
if __name__ == '__main__': 
    parser = argparse.ArgumentParser() 
  
    parser.add_argument('pythonfile') 
    args = parser.parse_args() 
    arcs = [] 
  
    cfg = PyCFG() 
    cfg.gen_cfg(slurp(args.pythonfile).strip()) 
    g = CFGNode.to_graph(arcs) 
    g.draw(args.pythonfile + '.png', prog ='dot') 
   
    print(g)

    nodes = g.number_of_nodes()     
    edges = g.number_of_edges()    
    complexity = edges - nodes + 2 
