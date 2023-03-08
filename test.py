import iterate

print(iterate.command("[US-W] --> [ALL]: echo hello world"))
print(iterate.command("[US-E] --> [US-W]: echo HI WEST!!!"))
print(iterate.command("[CA] --> [ALL]: echo hello world FROM CANADA!"))
print(iterate.command("[JPN] --> [US-W]: echo HI WEST!!!"))
