from resources.structures.Bloxlink import Bloxlink
from resources.exceptions import UserNotVerified, Message, Error
from discord import Embed

get_user, get_binds = Bloxlink.get_module("roblox", attrs=["get_user", "get_binds"])


@Bloxlink.command
class GetinfoCommand(Bloxlink.Module):
	"""retrieve the Roblox information from a member"""

	def __init__(self):
		self.aliases = ["whois"]
		self.arguments = [
			{
				"prompt": "Please specify the user.",
				"type": "user",
				"name": "target",
				"optional": True
			}
		]

		self.examples = [
			"justin",
			"@justin",
			"84117866944663552",
			"@justin --avatar",
			"@justin --avatar --groups"
		]
		self.cooldown = 5

	@Bloxlink.flags
	async def __main__(self, CommandArgs):
		target = CommandArgs.parsed_args["target"] or CommandArgs.message.author
		flags = CommandArgs.flags
		guild = CommandArgs.message.guild
		response = CommandArgs.response
		prefix = CommandArgs.prefix

		if target.bot:
			raise Message("Bots can't have Roblox accounts!", type="silly")

		valid_flags = ["username", "id", "avatar", "premium", "badges", "groups", "description", "age", "banned"]

		if not all(f in valid_flags for f in flags.keys()):
			raise Error(f"Invalid flag! Valid flags are: ``{', '.join(valid_flags)}``")

		#async with response.loading():
		role_binds, group_ids, _ = await get_binds(guild_data=CommandArgs.guild_data, trello_board=CommandArgs.trello_board)

		try:
			account, accounts = await get_user(*flags.keys(), author=target, guild=guild, group_ids=(group_ids, role_binds), send_embed=True, response=response, everything=not bool(flags), basic_details=not bool(flags))
		except UserNotVerified:
			raise Error(f"**{target}** is not linked to Bloxlink.")
		else:
			if not account:
				raise Message(f"You have no primary account set! Please use ``{prefix}switchuser`` and set one.", type="silly")

