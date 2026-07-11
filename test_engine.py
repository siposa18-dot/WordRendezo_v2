from word_engine import WordEngine

engine = WordEngine()

engine.open_word()

engine.open_document("02.docx")

print(engine.src.Name)

engine.create_document()

print("OK")

engine.close_word()