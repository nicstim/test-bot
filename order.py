from transitions import Machine
from fuzzywuzzy import fuzz

all_machine = dict()


class PizzaOrder(object):
    states = ["Какую вы хотите пиццу? Большую или маленькую?", 'Как вы будете платить?', "подтверждение",
              "Спасибо за заказ"]

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pizza_size = None
        self.payment = None
        self.machine = Machine(model=self, states=PizzaOrder.states, initial=PizzaOrder.states[0])
        self.machine.add_transition(trigger='size', source=PizzaOrder.states[0], dest=PizzaOrder.states[1],
                                    after='update_pizza_size')
        self.machine.add_transition(trigger='pay', source=PizzaOrder.states[1], dest=PizzaOrder.states[2],
                                    after='update_payment')
        self.machine.add_transition(trigger="no", source="*", dest=PizzaOrder.states[0], after="reset")
        self.machine.add_transition(trigger="yes", source=PizzaOrder.states[2], dest=PizzaOrder.states[3],
                                    after="success")

    def reset(self):
        self.pizza_size = None
        self.payment = None

    def update_pizza_size(self, **kwargs):
        self.pizza_size = kwargs.get("size")

    def update_payment(self, **kwargs):
        self.payment = kwargs.get("payment")

    def success(self):
        del all_machine[self.user_id]


def create_order(text: str, user_id: str) -> str:
    if not all_machine.get(user_id):
        all_machine[user_id] = PizzaOrder(user_id)
        return all_machine.get(user_id).state
    order = all_machine.get(user_id)
    state = order.state
    if fuzz.ratio("нет", text.lower()) > 70 or fuzz.ratio("отмена", text.lower()) > 70:
        order.no()
        return order.state
    if state == PizzaOrder.states[0] and text == "/start":
        return state
    elif state == PizzaOrder.states[0]:
        order.size(**{"size": text})
        return order.state
    elif state == PizzaOrder.states[1]:
        order.pay(**{"payment": text})
        return f"Вы хотите {order.pizza_size} пиццу, оплата - {order.payment}?"
    elif state == PizzaOrder.states[2] and fuzz.ratio("да", text.lower()) > 70:
        order.yes()
        return order.state
    else:
        return "Я вас не понял."

