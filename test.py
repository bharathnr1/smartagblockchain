class Hello:
    def check(self):
        checka = "checka"
        checkb = "checkb"
        return "Hello world"
    def mine(self):
        minea = 'minea'
        mineb = 'mineb'
        check1 = self.check
        print(str(check1))

d = Hello()
d.mine()
getattr(d, '')
b = Hello()
c = []

c.append(b)
c.append(d)

print(c)
