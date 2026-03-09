from zope.interface import Interface


class IConcept(Interface):
    """Concept -- cross-database concept."""


class IFeature(Interface):
    """Database-specific feature."""
