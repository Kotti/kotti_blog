# Copied from https://pypi.python.org/pypi/plone.batching.

class BaseBatch(object):
    """ A sequence batch splits up a large number of items over multiple pages
    """

    size = first = start = end = 0
    navlist = []
    numpages = pagenumber = pagerange = pagenumber = 0
    orphan = overlap = 0
    b_start_str = 'b_start'

    def __init__(self, sequence, size, start=0, end=0, orphan=0, overlap=0,
                 pagerange=7):
        """ Encapsulate sequence in batches of size
        sequence  - the data to batch.
        size      - the number of items in each batch.
        start     - the first element of sequence to include in batch
                    (0-index)
        end       - the last element of sequence to include in batch
                    (0-index, optional)
        orphan    - the next page will be combined with the current page
                    if it does not contain more than orphan elements
        overlap   - the number of overlapping elements in each batch
        pagerange - the number of pages to display in the navigation
        """
        start += 1
        self._sequence = sequence
        self._size = size
        self.orphan = orphan
        self.overlap = overlap
        self.pagerange = pagerange

        self.initialize(start, end, size)

    def initialize(self, start, end, size):
        """ Calculate effective start, end, length and pagesize values
        """
        start, end, sz = opt(start, end, size, self.orphan,
                             self.sequence_length)

        self.pagesize = sz
        self.start = start
        self.end = end

        self.first = max(start - 1, 0)
        self.length = self.end - self.first

        self.last = self.sequence_length - size

        # Set up the total number of pages
        self.numpages = calculate_pagenumber(
            self.sequence_length - self.orphan, self.pagesize, self.overlap)

        # Set up the current page number
        self._pagenumber = calculate_pagenumber(
            self.start, self.pagesize, self.overlap)

    @property
    def navlist(self):
        """ Pagenumber list for creating batch links """
        start = max(self.pagenumber - (self.pagerange / 2), 1)
        end = min(start + self.pagerange - 1, self.lastpage)
        return range(start, end + 1)

    def getPagenumber(self):
        return self._pagenumber

    def setPagenumber(self, pagenumber):
        """ Set pagenumber and update batch accordingly """
        start = max(0, (pagenumber - 1) * self._size) + 1
        self.initialize(start, 0, self._size)
        self._pagenumber = pagenumber

    pagenumber = property(getPagenumber, setPagenumber)

    @classmethod
    def fromPagenumber(cls, items, pagesize=20, pagenumber=1, navlistsize=5):
        """ Create new page from sequence and pagenumber
        """
        start = max(0, (pagenumber - 1) * pagesize)
        return cls(items, pagesize, start, pagerange=navlistsize)

    @property
    def sequence_length(self):
        """ Effective length of sequence
        """
        return getattr(self._sequence, 'actual_result_count',
                       len(self._sequence))

    def __len__(self):
        """ Alias of `sequence_length`
        """
        return self.sequence_length

    @property
    def next(self):
        """ Next batch page
        """
        if self.end >= (self.last + self.pagesize):
            return None
        return Batch(self._sequence, self._size, self.end - self.overlap,
            0, self.orphan, self.overlap)

    @property
    def previous(self):
        """ Previous batch page
        """
        if not self.first:
            return None
        return Batch(self._sequence, self._size,
            self.first - self._size + self.overlap, 0, self.orphan,
            self.overlap)

    def __getitem__(self, index):
        """ Get item from batch
        """
        actual = getattr(self._sequence, 'actual_result_count', None)
        if actual is not None and actual != len(self._sequence):
            # optmized batch that contains only the wanted items in the
            # sequence
            return self._sequence[index]
        if index < 0:
            if index + self.end < self.first:
                raise IndexError(index)
            return self._sequence[index + self.end]
        if index >= self.length:
            raise IndexError(index)
        return self._sequence[index + self.first]

    # methods from plone.app.content
    @property
    def firstpage(self):
        """ First page of batch

            Always 1
        """
        return 1

    @property
    def lastpage(self):
        """ Last page of batch
        """
        pages = self.sequence_length / self.pagesize
        if self.sequence_length % self.pagesize:
            pages += 1
        return pages

    @property
    def islastpage(self):
        """ True, if page is last page.
        """
        return self.lastpage == self.pagenumber

    @property
    def items_on_page(self):
        """ Alias for `length`
        """
        return self.length

    @property
    def multiple_pages(self):
        """ `True`, if batch has more than one page.
        """
        return bool(self.sequence_length / self.pagesize)

    @property
    def previouspage(self):
        """ Previous page
        """
        return self.pagenumber - 1

    @property
    def nextpage(self):
        """ Next page
        """
        return self.pagenumber + 1

    @property
    def items_not_on_page(self):
        """ Items of sequence outside of batch
        """
        return self._sequence[:self.first] + self._sequence[self.end:]

    @property
    def next_item_count(self):
        """ Number of elements in next batch
        """
        return self.next.length

    @property
    def has_next(self):
        """ Batch has next page
        """
        return self.next is not None

    @property
    def show_link_to_first(self):
        """ First page is in navigation list
        """
        return 1 not in self.navlist

    @property
    def show_link_to_last(self):
        """ Last page is in navigation list
        """
        return self.lastpage not in self.navlist

    @property
    def before_last_page_not_in_navlist(self):
        return (self.lastpage - 1) not in self.navlist

    @property
    def has_previous(self):
        return self.pagenumber > 1

    @property
    def previous_pages(self):
        return self.navlist[:self.navlist.index(self.pagenumber)]

    @property
    def next_pages(self):
        return self.navlist[self.navlist.index(self.pagenumber) + 1:]

    @property
    def second_page_not_in_navlist(self):
        return 2 not in self.navlist


class QuantumBatch(BaseBatch):
    """ A batch with quantum leaps for quicker navigation of large resultsets.

        (e.g. next 1 10 100 ... results )
    """
    quantumleap = False
    leapback = []
    leapforward = []

    def __init__(self, sequence, size, start=0, end=0, orphan=0, overlap=0,
                 pagerange=7, quantumleap=0):
        """
        quantumleap - 0 or 1 to indicate if bigger increments should be used
                      in the navigation list for big results.
        """
        self.quantumleap = quantumleap
        super(QuantumBatch, self).__init__(sequence, size, start, end, orphan,
                                           overlap, pagerange)

    def initialize(self, start, end, size):
        super(QuantumBatch, self).initialize(start, end, size)
        if self.quantumleap:
            self.leapback = calculate_leapback(
                self.pagenumber, self.numpages, self.pagerange)
            self.leapforward = calculate_leapforward(
                self.pagenumber, self.numpages, self.pagerange)

Batch = BaseBatch


def opt(start, end, size, orphan, sequence_length):
    """ Calculate start, end, batchsize
    """
    # This is copied from ZTUtils.Batch.py because orphans were not correct
    # there. 04/16/04 modified by Danny Bloemendaal (_ender_). Removed
    # try/except structs because in some situations they cause some unexpected
    # problems. Also fixed some problems with the orphan stuff.
    # Seems to work now.
    length = sequence_length
    if size < 1:
        if start > 0 < end >= start:
            size = end + 1 - start
        else:
            size = 25
    start = min(start, length)
    if end > 0:
        end = max(end, start)
    else:
        end = start + size - 1
        if (end + orphan) >= length:
            end = length
    return start, end, size


def calculate_pagenumber(elementnumber, batchsize, overlap=0):
    """ Calculate the pagenumber for the navigation """
    # To find first element in a page,
    # elementnumber = pagenumber * (size - overlap) - size (- orphan?)
    realsize = batchsize - overlap
    if realsize != 0:
        pagenumber, remainder = divmod(elementnumber, realsize)
    else:
        pagenumber, remainder = divmod(elementnumber, 1)
    if remainder > overlap:
        pagenumber += 1
    pagenumber = max(pagenumber, 1)
    return pagenumber


def calculate_pagerange(pagenumber, numpages, pagerange):
    """ Calculate the pagerange for the navigation quicklinks """
    # Pagerange is the number of pages linked to in the navigation, odd number
    pagerange = max(0, pagerange + pagerange % 2 - 1)
    # Making sure the list will not start with negative values
    pagerangestart = max(1, pagenumber - (pagerange - 1) / 2)
    # Making sure the list does not expand beyond the last page
    pagerangeend = min(pagenumber + (pagerange - 1) / 2, numpages) + 1
    return pagerange, pagerangestart, pagerangeend


def calculate_quantum_leap_gap(numpages, pagerange):
    """ Find the QuantumLeap gap. Current width of list is 6 clicks (30/5) """
    return int(max(1, round(float(numpages - pagerange) / 30)) * 5)


def calculate_leapback(pagenumber, numpages, pagerange):
    """ Check the distance between start and 0 and add links as necessary """
    leapback = []
    quantum_leap_gap = calculate_quantum_leap_gap(numpages, pagerange)
    num_back_leaps = max(0, min(3, int(round(
        float(pagenumber - pagerange) / quantum_leap_gap) - 0.3)))
    if num_back_leaps:
        pagerange, pagerangestart, pagerangeend = calculate_pagerange(
            pagenumber, numpages, pagerange)
        leapback = range(pagerangestart - num_back_leaps * quantum_leap_gap,
            pagerangestart, quantum_leap_gap)
    return leapback


def calculate_leapforward(pagenumber, numpages, pagerange):
    """ Check the distance between end and length and add links as necessary
    """
    leapforward = []
    quantum_leap_gap = calculate_quantum_leap_gap(numpages, pagerange)
    num_forward_leaps = max(0, min(3, int(round(
        float(numpages - pagenumber - pagerange) / quantum_leap_gap) - 0.3)))
    if num_forward_leaps:
        pagerange, pagerangestart, pagerangeend = calculate_pagerange(
            pagenumber, numpages, pagerange)
        leapforward = range(pagerangeend - 1 + quantum_leap_gap,
            pagerangeend - 1 + (num_forward_leaps + 1) * quantum_leap_gap,
            quantum_leap_gap)
    return leapforward
