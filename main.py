import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

DATA_FILE = 'notes.json'

@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: str

class NotesApp:
    def __init__(self, filename: str = DATA_FILE):
        self.filename = filename
        self.notes: List[Note] = []
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            self.notes = []
            return
        with open(self.filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                self.notes = [Note(**item) for item in data]
            except json.JSONDecodeError:
                self.notes = []

    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(note) for note in self.notes], f, ensure_ascii=False, indent=2)

    def add(self, title: str, content: str) -> Note:
        note_id = (max([n.id for n in self.notes]) + 1) if self.notes else 1
        note = Note(
            id=note_id,
            title=title,
            content=content,
            created_at=datetime.utcnow().isoformat()
        )
        self.notes.append(note)
        self._save()
        return note

    def remove(self, note_id: int) -> bool:
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self._save()
                return True
        return False

    def list_notes(self) -> List[Note]:
        return list(self.notes)

    def search(self, keyword: str) -> List[Note]:
        keyword_lower = keyword.lower()
        return [n for n in self.notes if keyword_lower in n.title.lower() or keyword_lower in n.content.lower()]

def print_note(note: Note):
    print(f"[{note.id}] {note.title} ({note.created_at})\n{note.content}\n")  # タイトル・本文はそのまま

def main():
    import argparse

    parser = argparse.ArgumentParser(description="シンプルなノートアプリ")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="ノートを追加")
    add_p.add_argument("title")
    add_p.add_argument("content")

    rm_p = subparsers.add_parser("remove", help="ノートを削除")
    rm_p.add_argument("id", type=int)

    list_p = subparsers.add_parser("list", help="ノートを一覧表示")

    search_p = subparsers.add_parser("search", help="ノートを検索")
    search_p.add_argument("keyword")

    args = parser.parse_args()
    app = NotesApp()

    if args.command == "add":
        note = app.add(args.title, args.content)
        print("ノートを追加しました：")
        print_note(note)
    elif args.command == "remove":
        success = app.remove(args.id)
        if success:
            print(f"ノート {args.id} を削除しました")
        else:
            print(f"ノート {args.id} が見つかりません")
    elif args.command == "list":
        for note in app.list_notes():
            print_note(note)
    elif args.command == "search":
        results = app.search(args.keyword)
        if results:
            print(f"{len(results)} 件のノートが見つかりました：")
            for note in results:
                print_note(note)
        else:
            print("該当するノートはありません")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
