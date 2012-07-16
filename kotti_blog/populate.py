"""Initialize kotti_blog in an existing Kotti database.

Usage:  python -m kotti_blog.populate  sqlite:///Kotti.db

This creates the additional tables needed. It leaves the tables empty (i.e., no
blogs).
"""

import argparse
import kotti_blog.resources as resources
import sqlalchemy as sa

def get_parser():
    parser = argparse.ArgumentParser()
    paa = parser.add_argument
    paa("dburl")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    engine = sa.create_engine(args.dburl, echo=True)
    conn = engine.connect()
    resources.Blog.__table__.create(bind=conn)
    resources.BlogEntry.__table__.create(bind=conn)

if __name__ == "__main__":  main()
