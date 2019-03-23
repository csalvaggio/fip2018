import subprocess

def get_interface_ip_address(interface='eth0'):
   args = ['ifconfig']
   p = subprocess.Popen(args, stdout=subprocess.PIPE)
   stdout = p.communicate()[0]

   ip = None
   inetFound = False
   interfaceFound = False
   components = stdout.decode().split(' ')
   for component in components:
      if inetFound:
         ip = component
         break

      subcomponents = component.split('\n')
      for subcomponent in subcomponents:
         if subcomponent == (interface + ':'):
            interfaceFound = True

      if interfaceFound:
         if component == 'inet':
            inetFound = True
         if component == 'RX':
            break

   return ip


if __name__ == '__main__':

   import network

   interface = 'eno1'
   ip = network.get_interface_ip_address(interface)
   print('IP address of interface "{0}" is {1}'.format(interface, ip))

