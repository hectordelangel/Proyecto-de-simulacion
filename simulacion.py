import numpy as np

class ClientType1():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "{} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class ClientType2():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "{} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Event():
    NEW_CLIENT1_ARRIVAL = 1
    NEW_CLIENT2_ARRIVAL = 2
    SUPERVISOR_EXIT = 3

    def __init__(self, time, event_type, client):
        self.time=time
        self.event_type=event_type
        self.client = client

    def __repr__(self):
        if self.event_type==self.NEW_CLIENT1_ARRIVAL:
            return "{:6.2f} - Entro al sistema el cliente tipo 1 {}".format(self.time, self.client.id)
        elif self.event_type==self.NEW_CLIENT2_ARRIVAL:
            return "{:6.2f} - Entro al sistema el cliente tipo 2{}".format(self.time, self.client.id)
        elif self.event_type==self.SUPERVISOR_EXIT:
            return "{:6.2f} - Cliente {} salio de supervision".format(self.time, self.client.id)
        else:
            return "{:6.2f} - Evento Desconocido".format(self.time)
        
def getTime(event):
    return event.time       

class Simulation():

    EMPTY = 0
    BUSY = 1

    def __init__(self):
        self.simulation_time = 0
        self.clock=0
        self.maxQueue=0
        self.events=[]
        self.queue=[]
        self.exits=[]
        self.client2Counts=0;
        self.supervisor_state = self.EMPTY
        self.prepare_entries()

    def prepare_entries(self):
        time1 = 0
        id = 1

        time2 = 0
        id2 = 1
        while True:
            if self.client2Counts <= 500:
                time1 += np.random.uniform(100,150)
                client = ClientType1(id)
                id+=1
                client.arrival_time = time1
                self.events.append(Event(time1,Event.NEW_CLIENT1_ARRIVAL, client))

                time2 += 120
                client2 = ClientType2(id2)
                id2+=1
                client2.arrival_time = time2
                self.events.append(Event(time2,Event.NEW_CLIENT2_ARRIVAL, client2))
                self.client2Counts+=1
            else:
                self.simulation_time=time2
                self.events.pop()
                break

    def next_event(self):
        event = self.events.pop(0); 
        # if event.event_type == event.NEW_CUSTOMER_ARRIVAL:
        self.clock = event.time 
        return event
        
    def run(self):
        while self.events:
            if(len(self.queue)+1>=self.maxQueue):
                self.maxQueue=len(self.queue)+1
            event = self.next_event()
            self.clock = event.time
            if event.event_type == event.NEW_CLIENT1_ARRIVAL:
                event.client.enter_queque_time = self.clock
                self.queue.append(event.client)
            if event.event_type == event.NEW_CLIENT2_ARRIVAL:
                event.client.enter_queque_time = self.clock
                self.queue.append(event.client)
            elif event.event_type == event.SUPERVISOR_EXIT:
                self.supervisor_state = self.EMPTY
                event.client.exit_supervisor_time=self.clock
                self.exits.append(event.client)

            if self.supervisor_state == self.EMPTY and len(self.queue)>0:
                self.supervisor_state = self.BUSY
                next_client = self.queue.pop(0)
                if type(next_client).__name__ == "ClientType1":
                    busy_time = np.random.exponential(25)
                else:
                    busy_time = np.random.gamma(2,(35/2))
                next_client.enter_supervisor_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.SUPERVISOR_EXIT, next_client))
                self.events.sort(key=getTime)
            if self.clock > self.simulation_time:
                break

sim = Simulation()
sim.run()


timeinsystem_type1_avg = 0
timeinsystem_type2_avg = 0
aux1=0
aux2=0
type1=[]
type2 = []
for client in sim.exits:
    if type(client).__name__ == "ClientType1":
        aux1+=client.exit_supervisor_time-client.arrival_time
        if timeinsystem_type1_avg:
            timeinsystem_type1_avg = timeinsystem_type1_avg+((client.exit_supervisor_time - client.arrival_time)-timeinsystem_type1_avg)/(len(type1)+1)
        else:
            timeinsystem_type1_avg = client.exit_supervisor_time - client.arrival_time
        type1.append((client.exit_supervisor_time,timeinsystem_type1_avg))
    elif type(client).__name__ == "ClientType2":
        aux2+=client.exit_supervisor_time-client.arrival_time
        if timeinsystem_type2_avg:
            timeinsystem_type2_avg = timeinsystem_type2_avg+((client.exit_supervisor_time - client.arrival_time)-timeinsystem_type2_avg)/(len(type2)+1)
        else:
            timeinsystem_type2_avg = client.exit_supervisor_time - client.arrival_time
        type2.append((client.exit_supervisor_time,timeinsystem_type2_avg))

print("Tiempo total de simulación {} minutos ".format(sim.simulation_time))
print("Fueron atendidos {} clientes tipo 1".format(len(type1)))
print("Fueron atendidos {} clientes tipo 2".format(len(type2)))
print("Tiempo promedio de estancia en la oficina para clientes tipo 1: {}".format(aux1/len(type1)))
print("Tiempo promedio de estancia en la oficina para clientes tipo 2: {}".format(aux2/len(type2)))
print("Máximo de clientes en la oficina: {}".format(sim.maxQueue))
