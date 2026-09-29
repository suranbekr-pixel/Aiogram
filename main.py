import asyncio
import os
import sys
from dotenv import load_dotenv

import dz_1
import dz_2
import dz_3
import dz_4

load_dotenv()

if __name__ == "__main__":
    print("=" * 55)
    print("🤖 AIOGRAM БОТТОРУН ТАНДОО:")
    print("=" * 55)
    print("1 -> 1-үй тапшырмасын иштетүү (dz_1.py)")
    print("2 -> 2-үй тапшырмасын иштетүү (dz_2.py)")
    print("3 -> 3-үй тапшырмасын иштетүү (dz_3.py - Ресторан)")
    print("4 -> 4-үй тапшырмасын иштетүү (dz_4.py - Катталуу FSM)")
    print("=" * 55)


    print("Демейки боюнча 1-үй тапшырмасы иштеп жатат...")
    asyncio.run(dz_1.main())
