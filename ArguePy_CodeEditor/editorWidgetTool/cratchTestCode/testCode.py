# help("keywords")
keyword = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
help("symbols")







class test:

    def __init__(self, *args, **kwargs):
        """
        ITA:
            Init è il metodo che viene chiamato quando si crea un oggetto di questa classe.
        ENG:
            Init is the method that is called when you create an object of this class.
        """
        self.arg = args

    def __str__(self):
        """
        ITA:
            Questo metodo viene chiamato quando si converte l'oggetto in una stringa.
        ENG:
            This method is called when you convert the object into a string.
        :return:
        """
        return str(self.arg)

    def __repr__(self):
        """
        ITA:
            Questo metodo viene chiamato quando si converte l'oggetto in una stringa. La differenze con
            __str__ è che __repr__ viene chiamato anche quando si stampa l'oggetto. per esempio:
            print(test(1,2,3)) -> <__main__.test object at 0x000001F1D1B5F0F0>
            in questo modo invece se la funzione è test(1,2,3) -> (1, 2, 3)
        ENG:
            This method is called when you convert the object into a string. The difference with
            __str__ is that __repr__ is also called when you print the object. for example:
            print(test(1,2,3)) -> <__main__.test object at 0x000001F1D1B5F0F0>
            in this way instead if the function is test(1,2,3) -> (1, 2, 3)
        :return:
        """
        return str(self.arg)

    def __call__(self, *args, **kwargs):
        """
        ITA:
            Questo metodo viene chiamato quando si chiama l'oggetto come una funzione. Ad esempio:
            se il codice è:
            a = test(1,2,3)
            a(4,5,6)
            allora il metodo __call__ viene chiamato con i parametri (4,5,6)
        ENG:
            This method is called when you call the object as a function.
            For example:
            if the code is:
            a = test(1,2,3)
            a(4,5,6)
            then the __call__ method is called with the parameters (4,5,6)
        :param args:
        :param kwargs:
        :return:
        """
        return self.arg

    def __len__(self):
        """docstring for __len__"""
        return len(self.arg)

    def __getitem__(self, key):
        """docstring for __getitem__"""
        return self.arg[key]

    def __setitem__(self, key, value):
        """docstring for __setitem__"""
        self.arg[key] = value

    def __delitem__(self, key):
        """docstring for __delitem__"""
        del self.arg[key]

    def __iter__(self):
        """docstring for __iter__"""
        return iter(self.arg)

    def __reversed__(self):
        """docstring for __reversed__"""
        return reversed(self.arg)

    def __contains__(self, item):
        """docstring for __contains__"""
        return item in self.arg

    def __add__(self, other):
        """docstring for __add__"""
        return self.arg + other

    def __sub__(self, other):
        """docstring for __sub__"""
        return self.arg - other

    def __mul__(self, other):
        """docstring for __mul__"""
        return self.arg * other

    def __matmul__(self, other):
        """docstring for __matmul__"""
        return self.arg @ other

    def __truediv__(self, other):
        """docstring for __truediv__"""
        return self.arg / other

    def __floordiv__(self, other):
        """docstring for __floordiv__"""
        return self.arg // other

    def __mod__(self, other):
        """docstring for __mod__"""
        return self.arg % other



    """"
    la lista dei __metodi__ è molto lunga, per vedere tutti i metodi che si possono sovrascrivere
    si può usare il comando help("special") non funziona perchè? non so, ma non funziona
    quindi copilot mi scrive una lista di tutti i metodi che si possono sovrascrivere
    lista 
    Certamente, ecco una lista di alcuni dei metodi speciali che è possibile sovrascrivere quando si definisce una classe in Python:

    __init__: viene chiamato quando un oggetto della classe viene creato e inizializzato, e viene utilizzato per eseguire qualsiasi operazione di inizializzazione necessaria.
    __str__: restituisce una rappresentazione testuale dell'oggetto, utilizzata ad esempio quando viene chiamata la funzione print.
    __repr__: restituisce una rappresentazione testuale dell'oggetto che può essere usata per riprodurlo, ad esempio quando viene chiamata la funzione eval.
    __len__: restituisce la lunghezza dell'oggetto quando viene chiamata la funzione len.
    __getitem__: permette di accedere agli elementi dell'oggetto mediante l'utilizzo dell'operatore [].
    __setitem__: permette di modificare gli elementi dell'oggetto mediante l'utilizzo dell'operatore [].
    __delitem__: permette di eliminare gli elementi dell'oggetto mediante l'utilizzo dell'operatore [].
    __iter__: restituisce un iteratore per l'oggetto, utilizzabile ad esempio in un ciclo for.
    __next__: restituisce il prossimo elemento nell'iterazione quando viene chiamato l'iteratore restituito da __iter__.
    __eq__: restituisce True se l'oggetto è uguale a un altro oggetto specificato.
    __ne__: restituisce True se l'oggetto è diverso da un altro oggetto specificato.
    __lt__: restituisce True se l'oggetto è minore di un altro oggetto specificato.
    __le__: restituisce True se l'oggetto è minore o uguale a un altro oggetto specificato.
    __gt__: restituisce True se l'oggetto è maggiore di un altro oggetto specificato.
    __ge__: restituisce True se l'oggetto è maggiore o uguale a un altro oggetto specificato.
    __add__: restituisce la somma dell'oggetto con un altro oggetto specificato.
    __sub__: restituisce la differenza tra l'oggetto e un altro oggetto specificato.
    __mul__: restituisce il prodotto dell'oggetto con un altro oggetto specificato.
    __truediv__: restituisce la divisione tra l'oggetto e un altro oggetto specificato.
    __floordiv__: restituisce la divisione intera tra l'oggetto e un altro oggetto specificato.
    __mod__: restituisce il resto della divisione tra l'oggetto e un altro oggetto specificato.
    __pow__: restituisce l'oggetto elevato alla potenza di un altro oggetto specificato.
    __radd__: restituisce la somma di un altro oggetto specificato con l'oggetto.
    __rsub__: restituisce la differenza tra un altro oggetto specificato e l'oggetto.
    """

    specials = ["__init__", "__str__", "__repr__", "__len__", "__getitem__", "__setitem__", "__delitem__", "__iter__", "__next__", "__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__", "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__", "__mod__", "__pow__", "__radd__", "__rsub__"]





































































































































































































