import asyncio
import git
import hashlib
import os


async def clone_rep(repo_url, destination, loop):
    print(f'START LOADING {repo_url}')
    try:
        await loop.run_in_executor(
            None, git.Repo.clone_from, repo_url, destination)
        print(f'FINISH LOADING {repo_url}')
        return True
    except Exception as e:
        print(f'Failed to load {repo_url}. Reason: {e}')
        return False


def dir_hash(directory, verbose=0):
    sha_hash = hashlib.sha256()
    if not os.path.exists(directory):
        return -1

    try:
        for root, dirs, files in os.walk(directory):
            for names in sorted(files):
                filepath = os.path.join(root, names)
                if verbose == 1:
                    print(f'Hashing {filepath}')
                try:
                    f1 = open(filepath, 'rb')
                except Exception as e:
                    # You can't open the file for some reason
                    print(e)
                    f1.close()
                    continue

                while 1:
                    # Read file in as little chunks
                    buf = f1.read(4096)
                    if not buf:
                        break
                    h = hashlib.sha256(buf)
                    d = h.hexdigest().encode('utf-8')
                    sha_hash.update(d)
                print(sha_hash.hexdigest())
                f1.close()

    except Exception as e:
        print(e)
        return -2
    res = sha_hash.hexdigest()
    print(res)
    return res


async def clone_all(root):
    repo_url = "https://gitea.radium.group/radium/project-configuration"
    loop = asyncio.get_event_loop()
    res = await asyncio.gather(
        clone_rep(repo_url, os.path.join(root, "1"), loop),
        clone_rep(repo_url, os.path.join(root, "2"), loop),
        clone_rep(repo_url, os.path.join(root, "3"), loop)
    )
    hashes = []
    if res[0]:
        hashes.append(dir_hash(os.path.join(root, "1"), 1))
    if res[1]:
        hashes.append(dir_hash(os.path.join(root, "2"), 1))
    if res[2]:
        hashes.append(dir_hash(os.path.join(root, "3"), 1))

    return hashes

if __name__ == "__main__":
    asyncio.run(clone_all("data"))
