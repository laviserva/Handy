def load_src(cpp_file):
    out = []
    with open(cpp_file, "r") as cpp:
        for line in cpp:
            out.append(line)
        return "".join(out)