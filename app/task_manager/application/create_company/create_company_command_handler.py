from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_company.create_company_command import CreateCompanyCommand
from task_manager.domain.company.company_creator import CompanyCreator
from task_manager.domain.company.company_repository import CompanyRepository


class CreateCompanyCommandHandler(CommandHandler):
    def __init__(self, company_repository: CompanyRepository, company_creator: CompanyCreator):
        self.__company_repository = company_repository
        self.__company_creator =company_creator

    def handle(self, command: CreateCompanyCommand) -> None:
        company = self.__company_creator.create_company(
            company_id = command.company_id,
            name=command.name
        )

        self.__company_repository.save_company(company)
