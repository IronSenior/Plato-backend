from uuid import UUID


class ReportId:

    def __init__(self, reportId: UUID):
        self.checkUniqueId(reportId)
        self.checkIdVersion(reportId)
        self.__value: UUID = reportId

    @staticmethod
    def fromString(reportId: str):
        return ReportId(UUID(reportId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, reportId: UUID):
        if type(reportId) != UUID:
            raise TypeError("Account ID must be an UUID instance")

    def checkIdVersion(self, reportId: UUID):
        if reportId.version != 4:
            raise TypeError("Account ID must be version 4")
