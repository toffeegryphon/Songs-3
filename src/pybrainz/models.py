class Artist(object):
    uid: str
    name: str
    """
    Artist class containing name and uid
    """
    def __init__(self, uid: str, name: str):
        """
        Initialise uid and name

        :param uid: MusicBrainz unique-id
        :type uid: str
        :param name: MusicBrainz display name
        :type name: str
        """
        # TODO Error if null?
        self.uid = uid
        self.name = name
    
    def __eq__(self, other) -> bool:
        """
        Override __eq__ to check equality based on properties.
        To check same reference, use `is`

        :param other: comparison element
        :type other: any
        :return: True if of same object and properties equal, false otherwise
        :rtype: bool
        """
        return isinstance(self, other.__class__) and self.__dict__ == other.__dict__