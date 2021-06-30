if exist gpynance\utils\numbautils* (
   python test.py test
   
) else (
   python gpynance\utils\_numbautils.py
   python test.py test
)

