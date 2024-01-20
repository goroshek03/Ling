#encoding "utf-8"
#GRAMMAR_ROOT Title

Attractions -> Word<kwtype=attractions>;
Title -> Attractions interp(AttractionsFact.Title);