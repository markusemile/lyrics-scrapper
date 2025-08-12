from colorama import Style, Fore, Back
from enum import Enum


def info(txt: str):
    return input(f"{Fore.GREEN}{txt}{Style.RESET_ALL}\n").strip().lower()


def error(txt: str):
    return input(f"{Back.RED}{Fore.BLACK}{txt}{Style.RESET_ALL}\n").strip().lower()


def in_green(txt: str):
    return f"{Fore.GREEN}{txt}{Style.RESET_ALL}"

