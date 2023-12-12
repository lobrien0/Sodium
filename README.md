# Sodium

The following program is a tool designed to check the passwords of
existing user-accounts against a list of potentially hazardous passwords

These passwords could be sourced from a large data-breach, a common passwords list,
or from many other sources. 

The goal is to help system administrators identify potentially risky accounts.

### Requirements:

- Must have a python version lower than `python 3.13` as the crypt library will be removed in later version (working on updating code)
- Must be run on a Unix-based system as the current implementation is designed for shadow files

### Recommendations:

Sodium is a resource intensive program, because of this, its is recommended that you run the program on a multi-core system.  
The code is designed to adapt to your available resources though, so this is not required.

## How to Run:

In order to run the code, input the following command while in the working directory:

```bash
python manage.py <shadow_file> <password_file>
```
> The `shadow_file` should be a unix-generated password file

> the `password_file` should be a list of passwords that you're checking against

> Note: depending on how you have python set up, you may have to substitute `python`
> with one of the following:  
> `python3`, `py`, `py3`

--
Example with the provided testing resources:

```bash
python manage.py test_shadow top100k.txt
```

## Limitations

Currently all common unix crypto-systems are supported with exception of `Yes-Crypt`.  
This is due to the overall complexity of the crypto-system.

This will be addressed in future implementations, but `Yes-Crypt` is intentionally designed to be difficult to post-process.  
Because of this, the implementation would be slow and computationally very expensive to verify.

If you'd like to learn more about this crypto-system, I highly recommend you visit the [GitHub: OpenWall/YesCrypt](https://github.com/openwall/yescrypt)

## Passwd_list.py

This is just an extra file put together to generate about 20MB worth of passwords using the top 1,000 words and Country names.  
(It generates the passwords surprisingly fast)

## Limited Lability Statement

The authors of this tool do not condone the use of the `Sodium` tool for anything other than permitted auditing and/or testing on authorized systems.

We will not be held responsible for any misuse of the tool under any circumstances.
