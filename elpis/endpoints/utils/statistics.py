from typing import Dict, NewType, List
import itertools
import re
import wave


def parse_grapheme_frequency_from_dataset(
    phrases: List[str],
    graphemes: List[str]
) -> Dict[str, int]:
    """
    Given a list of phrases, returns the frequency of the provided graphemes.
    """
    matcher = construct_grapheme_matcher(graphemes)
    result = {}
    for phrase in phrases:
        for word in phrase.split(" "):
            graphemes = word_to_graphemes(word, graphemes, matcher=matcher)
            for grapheme in graphemes:
                result[grapheme] = result.get(grapheme, 0) + 1
    return result


def word_to_graphemes(
    word: str,
    graphemes: List[str],
    matcher=None
) -> List[str]:
    """
    Takes a string and a grapheme matcher and returns the list of graphemes.
    """
    if matcher is None:
        matcher = construct_grapheme_matcher(graphemes)
    result = []
    r = matcher(word)
    while r is not None:
        # Append the grapheme to the result, r.start() will always be 0
        result.append(word[r.start():r.end()])
        # Trim the word to remove the found grapheme
        word = word[r.end():]
        # Attempt to find the next grapheme
        r = matcher(word)
    return result


def construct_grapheme_matcher(graphemes: List[str]):
    """
    Compiles a regex from a list of provided prefixes.

    This regex matches grapheme prefixes.

    Note: The matcher will sort the provided prefixes longest to shortest to
    guarantee that longer graphemes are found first.
    """
    regex_text = "|".join(re.escape(g)
                          for g in sorted(graphemes, key=len, reverse=True))
    return re.compile(regex_text).match


def get_length_of_wav(file_name):
    """
    Returns the length of a wav file in seconds.
    """
    with wave.open(str(file_name), 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

        
def generate_word_sankey(annotations: List[str]):
    """
    Generates sankey data for a list of annotations.
    """
    nodes = []
    links = {}
    for annotation in annotations:
        previous, current = itertools.tee(annotation.split(" "))
        previous = itertools.chain([None], previous)
        for p, c in zip(previous, current):
            if c not in nodes:
                nodes.append(c)
            if p is None or c is None:
                continue
            links[(p, c)] = links.get((p, c), 0) + 1
    return {
        "nodes": [ {"id": node} for node in nodes],
        "links": [ {
            "source": source,
            "target": target,
            "value": value
            } for (source, target), value in links.items()]
    }

def generate_grapheme_sankey(annotations: List[str], graphemes: List[str]):
    """
    Generates sankey data for a list of annotations.
    """
    nodes = []
    links = {}
    matcher = construct_grapheme_matcher(graphemes)
    for annotation in annotations:
        for word in annotation.split(" "):
            graphs = word_to_graphemes(word, graphemes, matcher=matcher)
            previous, current = itertools.tee(graphs)
            previous = itertools.chain([None], previous)
            for p, c in zip(previous, current):
                if c not in nodes:
                    nodes.append(c)
                if p is None or c is None:
                    continue
                links[(p, c)] = links.get((p, c), 0) + 1
    return trim_weak_circular_links(
        [{
            "source": source,
            "target": target,
            "value": value
        } for (source, target), value in links.items()],
        [{"id": node} for node in nodes]
    )


def split_list(list_):
    """
    Splits a list into two halves.
    """
    return (list_[:len(list_)//2], list_[len(list_)//2:])


def links_from(nodesA, nodesB, links):
    """
    Finds the links that go from nodesA to nodesB.
    """
    return [link for link in links if link["source"] in nodesA and link["target"] in nodesB]


def remove_links(links, remove_links):
    """
    Removes links from the given links that are in remove links.
    """
    return [link for link in links if link not in remove_links]


def shed_less_links(nodesA, nodesB, links):
    """
    Removes the links either A -> B or B -> A depending on which has less value. Preserves higher value cycles.    
    """
    links_from_b = links_from(nodesB, nodesA, links)
    links_from_a = links_from(nodesA, nodesB, links)
    if sum(map(lambda x: x["value"], links_from_a)) > sum(map(lambda x: x["value"], links_from_b)):
        return remove_links(links, links_from_b)
    else:
        return remove_links(links, links_from_a)


def do_trim_circular_links(nodes, links):
    """
    Trims circular links from a list of nodes and links.
    """
    if len(nodes) <= 1:
        return links
    listA, listB = split_list(nodes)
    links = shed_less_links(listA, listB, links)
    linksA = do_trim_circular_links(listA, links)
    return do_trim_circular_links(listB, linksA)

def trim_weak_circular_links(links: List[Dict], nodes: List[Dict]):
    """
    Trims weaker circular links from a list of links.

    To do this we perform a depth first search from the strongest link.
    """
    valid_links = do_trim_circular_links(list(map(lambda x: x["id"], nodes)), links)
    valid_nodes = set([link["target"] for link in links]).union(set([link["source"] for link in links]))
    return {
        "links": valid_links,
        # Trim any nodes that get left out :(
        "nodes": [node for node in nodes if node["id"] in valid_nodes]
    }