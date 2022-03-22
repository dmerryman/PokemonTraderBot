import discord

def getUserID(ctx, userName):
    member = ctx.guild.get_member_named(userName)
    if member is None:
        return None
    return member.id