""" Google R """


async def _init() -> None:
    os.system(
        "wget -c https://raw.githubusercontent.com/jarun/googler/v4.3.2/googler &&  chmod +x googler"
    )