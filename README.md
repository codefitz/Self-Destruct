# Self Destruct
 
  Self-destruct function for use in other projects, or temporary granting of use.

  CAUTION: This script will self-destruct without a key! Do not commit changes if accidentally run.

## Generating and Using a Key

1. Run `generate_key.py` to create a key with a 30 day lifetime:

   ```bash
   $ python3 generate_key.py
   Generating key, expiry date:  <date>
   Generated Key: <base64 string>

   Key will expire in 30 days.
   ```

   The produced key is a base64 encoded Python list in the form
   `[TIMESTAMP, 'random_key']`. `TIMESTAMP` is a Unix epoch value denoting the
   expiration time.

2. Supply the key to `self-destruct.py`:

   ```bash
   $ python3 self-destruct.py -k <base64 key>
   ```

   Use `--fakeout` to display debugging output instead of deleting the file.

`self-destruct.py` compares the timestamp with the current date and removes
itself when the key has expired.
