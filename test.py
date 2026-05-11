import re as regex;



title = "title [tag] [tag2] [tag 3 and also 4]"
print([t.upper().replace(" ", "-") for t in regex.findall(r"\[([^\[\]]+)\]", title)])
