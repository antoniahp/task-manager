from uuid import UUID


class UserDoesNotBelongToCompanyException(Exception):
    def __init__(self, requester_user_id: UUID, company_id: UUID):
        self.requester_user_id = requester_user_id
        self.company_id = company_id
        self.message = f"The user with ID {requester_user_id} tried to access the company with ID {company_id}, this user does not belong to the company."
        super().__init__(self.message)
