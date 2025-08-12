from typing import Any
from app_utils import wipe_screen, error
from app_utils.log_logger import get_logger
from config import KeyValue
from decorators import validate_return


@validate_return(context="paginateData")
def paginate_data(
        dico: Any | None = None,
        page: int | None = None,
        hint_to_display: KeyValue = KeyValue.VALUE,
        hint_to_return: KeyValue = KeyValue.KEY,
        expect_return: bool = True,
        title: str = "List of items",
        next_page: int | None = None
) -> Any:
    """
    function to display a list with pagination, can also return a choice
    :param next_page: int
    :param title: str: title menu
    :param dico: passed list any format
    :param page: int: the current page
    :param hint_to_display: str: the element to use to display
    :param hint_to_return: str: the element to use like a key
    :param expect_return: bool: expect a return value
    :return: Any type
    """
    logger = get_logger()

    if dico is None:
        logger.error("no dico passed")
        error("You must give a dico param")
        input("[enter] to continue...")

    t = [(len(title) + 2) * "*", f" {title} ", (len(title) + 2) * "*"]

    items_to_return = list()
    maxi = len(dico)
    # begin to display
    while True:
        wipe_screen()
        print("\n".join(t))
        for idx, (key, value) in enumerate(dico.items()):
            items_to_return.append(key if hint_to_return == KeyValue.KEY else value)
            print(f"[{idx}]: {value if hint_to_display == KeyValue.VALUE else key}")

        print(f"page={page}")
        option = ["=>", " [+] next " if page and next_page is not None else "", " [x] cancel ", "[-] prev " if page is not None and page > 1 else ""]
        print("".join(option))
        choice = input("Make your choice :").strip()

        if choice == "+":
            if next_page:
                return "next"
        elif choice == "-":
            if page > 0:
                return "prev"
        elif choice == "x":
            return None
        elif choice.isdigit() and int(choice) in range(0, maxi):
            if expect_return:
                return str(items_to_return[int(choice)])

        error("Please make a choice between [0 - {maxi-1}] \n")
        input(" [enter] to continue...")

