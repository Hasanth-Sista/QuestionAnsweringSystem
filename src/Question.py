def typeOfQuestion(question):
    tokens = question.split(" ")
    if "Who" == tokens[1] or "who" == tokens[1]:
        return ("PERSON", "NORP")
    elif "When" == tokens[1] or "when" == tokens[1]:
        return ("DATE", "TIME", "CARDINAL")
    elif "Where" == tokens[1] or "where" == tokens[1]:
        return ("LOC", "GPE", "EVENT")
