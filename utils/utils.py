"""
Utils
"""

# OS
from os.path import dirname, join

# Discord
import discord


root_dirname = dirname(dirname(__file__))


def get_file_path(file_path):
    """Get absolute file path"""
    return join(root_dirname, file_path)


# pylint: disable=fixme
# TODO: Properly check for each fields existence and set values.
# eg; Currently assumes title, description, color will be in 'embed_object',
# same for inner objects of 'fields', author object.
# pylint: disable=inconsistent-return-statements
def create_embed(embed_object):
    """Helper function to create embed for discords"""
    try:
        embed = discord.Embed(
            title=embed_object.title,
            description=embed_object.description,
            color=embed_object.color,
        )

        if hasattr(embed_object, "author"):
            embed.set_author(
                name=embed_object.author["name"],
                url=f"{embed_object.author['url']}",
                icon_url=embed_object.author["icon_url"],
            )

        if hasattr(embed_object, "thumbnail"):
            embed.set_thumbnail(url=f"{embed_object.thumbnail}")

        if hasattr(embed_object, "fields"):
            for field in embed_object.fields:
                embed.add_field(
                    name=field["name"],
                    value=field["value"],
                    inline=field["inline"],
                )

        return embed
    # pylint: disable=broad-except
    except Exception as e_values:
        print("error embed")
        print(e_values)
