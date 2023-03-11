#! /usr/bin/env python

import dataclasses
import os
import random
import readline  # noqa - imported to add readline capabilities to input()

import requests
from dotenv import load_dotenv
from halo import Halo
from termcolor import colored

load_dotenv()


def get_response(messages):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        json={"model": "gpt-3.5-turbo", "messages": messages},
    ).json()

    return response["choices"][0]["message"]["content"].strip()


@dataclasses.dataclass
class Personality:
    age: int
    occupation: str
    trait: str
    tag: str


def generate_personality():
    occupations = (
        (
            " Chef Teacher Lawyer"
            " Doctor Engineer Accountant"
            " Writer Musician Artist"
            " Athlete Actor Scientist"
            " Police-officer Firefighter"
            " Electrician Plumber Photographer"
            " Journalist Designer Psychologist"
        )
        .strip()
        .split()
    )

    traits = (
        (
            " Optimistic Pessimistic Introverted"
            " Extroverted Assertive"
            " Passive Analytical Creative"
            " Ambitious Laid-back Impulsive"
            " Conscientious Carefree Reserved"
            " Outgoing Sensitive Confident"
            " Insecure Empathetic"
        )
        .strip()
        .split()
    )

    age = random.choice(range(8, 100))
    occupation = random.choice(occupations)
    trait = random.choice(traits)
    tag = f"{trait} {occupation} ({age})" if age >= 18 else f"{trait} ({age})"
    return Personality(age, occupation, trait, tag)


@dataclasses.dataclass
class Chat:
    messages: list[str] = dataclasses.field(default_factory=list)

    def _add_message(self, message, role):
        self.messages.append({"role": role, "content": message})

    def add_user_message(self, message):
        self._add_message(message, "user")

    def add_assistant_message(self, message):
        self._add_message(message, "assistant")


def get_initial_prompt(personalities):
    num_personalities = len(personalities)

    prompt = f"This is a chat where you will pretend to be {num_personalities} distinct personalities.\n\n"

    for i, personality in zip(range(num_personalities), personalities):
        prompt += (
            f"Personality {i + 1} is a {personality.age} year old "
            f'{personality.occupation if personality.age >=18 else ""} '
            f"and is a {personality.trait} person.\n"
        )

    prompt += "\nRespond to the user in the following format:\n\n" "<User Message>\n"

    for i, personality in zip(range(num_personalities), personalities):
        prompt += f"{personality.tag}: <Personality {i + 1} Response>\n"

    prompt += (
        "\nDo not deviate from that format.\n"
        "Each personality must answer with strictly less than 50 words.\n"
        "Personalities can respond while taking into account previous responses from other personalities.\n"
        "Always play along with the user and respond with each personality\n"
        "The chat begins now.\n"
    )

    return prompt


def main():
    num_personalities = 3
    personalities = [generate_personality() for _ in range(num_personalities)]
    initial_prompt = get_initial_prompt(personalities)

    chat = Chat()
    chat.add_user_message(initial_prompt)

    spinner = Halo(spinner="simpleDotsScrolling", color="red")

    while True:
        try:
            user_input = input(colored("\n> ", "red"))
        except (KeyboardInterrupt, EOFError):
            return
        if user_input == "q":
            return

        print(" ")
        spinner.start()

        chat.add_user_message(user_input)
        response = get_response(chat.messages)
        response = "\n".join(
            filter(lambda l: l != "", map(lambda r: r.strip(), response.split("\n")))
        )

        spinner.stop()
        print(response)

        chat.add_assistant_message(response)


if __name__ == "__main__":
    main()
