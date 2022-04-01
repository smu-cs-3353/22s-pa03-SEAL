import networkx as nx
from networkx import graphml
import hashlib


# Filenames for conversion
inFile = "../ourDatasets/football/football.graphml"               # File to convert
cmtyFile = "../ourDatasets/football/football-1.90.cmty.txt"       # File to store communities
ungraphFile = "../ourDatasets/football/football-1.90.ungraph.txt" # File to store graph structure

# Variables for value mapping
mpaVals = True                                          # If True, map the values to other values,
                                                        # otherwise don't has the text
hashFile = "../ourDatasets/football/football_map.txt"   # Stores info on the hash conversion




# Load in the graph
G = graphml.read_graphml(inFile)


# Hash the node values if mpaVals is True
if mpaVals == True:
    nodes = list(G.nodes)
    assert type(nodes[0]) == str, "Nodes are not text"
    
    # The conversion map
    hashes = dict()
    
    # Iterate over every node
    for i in range(0, len(nodes)):
        n = nodes[i]
        
        # Add the value to the map
        if str(n)[:2] == "b'":
            hashes[str(n)[2:-1]] = i
        else:
            hashes[n] = i



# Open the output files for writing
cmty = open(cmtyFile, "w")
ungraph = open(ungraphFile, "w")


# Get the communities from the graph
communities = dict()
nodes = G.nodes._nodes
for n in nodes.keys():
    try:
        communities[nodes[n]["value"]].append(n)
    except KeyError:
        communities[nodes[n]["value"]] = [n]

# Save the communities to the cmty file
for c in communities.keys():
    for l in communities[c][:-1]:
        if mpaVals == True:
            l = hashes[l]
        cmty.write(f"{l} ")
    if mpaVals == True:
        cmty.write(f"{hashes[communities[c][-1]]}\n")
    else:
        cmty.write(f"{communities[c][-1]}\n")


# Get all the edges from the graph
edges = list(G.edges)


# Save the edges to the ungraph file
for e in edges[:-1]:
    if mpaVals == True:
        ungraph.write(f"{hashes[e[0]]} {hashes[e[1]]}\n")
    else:
        ungraph.write(f"{e[0]} {e[1]}\n")

if mpaVals == True:
    ungraph.write(f"{hashes[edges[-1][0]]} {hashes[edges[-1][1]]}")
else:
    ungraph.write(f"{edges[-1][0]} {edges[-1][1]}")


# Close the files
cmty.close()
ungraph.close()



# If the data is mapped, create a dictionary info file
if mpaVals == True:
    # Open the file
    f = open(hashFile, "w")
    
    # Write all parts of the dictionary to the file
    for k in list(hashes.keys())[:-1]:
        f.write(f"{hashes[k]}:{k}\n")
    f.write(f"{hashes[list(hashes.keys())[-1]]}:{list(hashes.keys())[-1]}")
    
    # Close the file
    f.close()