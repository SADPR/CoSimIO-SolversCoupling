import CoSimIO
info = CoSimIO.Hello()
print(info)

major_version = info.GetInt("major_version")
minor_version = info.GetInt("minor_version")
patch_version = info.GetString("patch_version")

print(f"CoSimIO version: {major_version}.{minor_version}.{patch_version}")
