import networkx as nx
import plotly.graph_objs as go


def make_edge(x, y, text, width):
    
    '''Creates a scatter trace for the edge between x's and y's with given width

    Parameters
    ----------
    x    : a tuple of the endpoints' x-coordinates in the form, tuple([x0, x1, None])
    
    y    : a tuple of the endpoints' y-coordinates in the form, tuple([y0, y1, None])
    
    width: the width of the line

    Returns
    -------
    An edge trace that goes between x0 and x1 with specified width.
    '''
    return go.Scatter(x=x,
                      y=y,
                      line=dict(width=width,
                                color='cornflowerblue'),
                      hoverinfo='none',
                      text=([text]),
                      mode='lines')


def get_network_traces(top_characters, top_pairs, pair_chars):
    dialogue = nx.Graph()
    
    # add node for each character
    for char, count in top_characters.iteritems():
        if char in pair_chars:
            dialogue.add_node(char, size=count)
        
    # for each dialogue exchange between two character add an edge
    for pair, count in top_pairs.iteritems():
        char1, char2 = pair.split('-')
        dialogue.add_edge(char1, char2, weight=count)
        
    # get positions for nodes
    pos_ = nx.spring_layout(dialogue)
    
    # for each edge make edge trace, append to list
    edge_trace = []
    for edge in dialogue.edges():
        if dialogue.edges()[edge]['weight'] > 0:
            char1 = edge[0]
            char2 = edge[1]

            x0, y0 = pos_[char1]
            x1, y1 = pos_[char2]

            text   = char1 + '--' + char2 + ': ' + str(dialogue.edges()[edge]['weight'])
            trace  = make_edge([x0, x1, None], [y0, y1, None], text,
                               0.15*dialogue.edges()[edge]['weight']**0.6)
            edge_trace.append(trace)
            
    # make a node trace
    node_trace = go.Scatter(x         = [],
                            y         = [],
                            text      = [],
                            textposition = "top center",
                            textfont_size = 10,
                            mode      = 'markers+text',
                            hoverinfo = 'none',
                            marker    = dict(color = [],
                                             size  = [],
                                             line  = None,
                                             reversescale=True
                                            ))
    # For each node in dialogue, get the position and size and add to the node_trace
    for node in dialogue.nodes():
        x, y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple(['cornflowerblue'])
        node_trace['marker']['size'] += tuple([dialogue.nodes()[node]['size']**0.75])
        node_trace['text'] += tuple(['<b>' + node + '</b>'])
        
    return edge_trace, node_trace
