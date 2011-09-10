import time
import fractions


HOUR_BASE = 24
MIN_BASE = 60
SEC_BASE = 60

def calc_time(num, denum):
  f = fractions.Fraction(num, denum)
  return "%d/%d" % (f.numerator, f.denominator)
  
def get_time(hour, min, sec):
  text = "%s %s %s" % (calc_time(hour, HOUR_BASE),calc_time(min, MIN_BASE),calc_time(sec, SEC_BASE))
  return text
  
def get_current_time():
  hour = time.localtime().tm_hour
  min = time.localtime().tm_min
  sec = time.localtime().tm_sec
  return get_time(hour, min, sec)

if __name__ == '__main__':
  while True:
    print get_current_time()
    time.sleep(1)
