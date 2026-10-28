from .models import Item
from decimal import Decimal




def check_stock(name):
    """Look up an item's quantity and unit price."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
    }




def list_items():
    """Return every item in the inventory with its price."""
    items = Item.objects.all()

    return {
        "items": [
            {
                "name": i.name,
                "quantity": i.quantity,
                "price": float(i.price),
            }
            for i in items
        ]
    }



def add_item(name, quantity):
    """Create a new item, or add to an existing one's stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is not None:
        item.quantity += quantity
        item.save()
        return {"name": item.name, "quantity": item.quantity, "created": False}
    item = Item.objects.create(name=name, quantity=quantity)
    return {"name": item.name, "quantity": item.quantity, "created": True}


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
        }
    item.quantity -= quantity
    item.save()
    return {"name": item.name, "quantity": item.quantity}


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    item.delete()
    return {"deleted": name}


def calculate_cost(name, quantity, vat_percentage):
    """Calculate the total cost of items including VAT."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    if quantity <= 0:
        return {"error": "Quantity must be positive."}

    if vat_percentage < 0:
        return {"error": "VAT percentage cannot be negative."}

    
    vat_percentage = Decimal(str(vat_percentage))
    unit_price = item.price
    subtotal = unit_price * quantity
    vat_amount = subtotal * vat_percentage / 100
    total = subtotal + vat_amount

    return {
        "name": item.name,
        "quantity": quantity,
        "unit_price": float(unit_price),
        "subtotal": round(float(subtotal), 2),
        "vat_percentage": float(vat_percentage),
        "vat_amount": round(float(vat_amount), 2),
        "total": round(float(total), 2),
    }
def increase_price(name, percentage):
    """Increase an item's price by a given percentage."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    if percentage < 0:
        return {"error": "Percentage cannot be negative."}

    percentage = Decimal(str(percentage))

    old_price = item.price
    increase_amount = old_price * percentage / 100
    new_price = old_price + increase_amount

    item.price = new_price
    item.save()

    return {
        "name": item.name,
        "old_price": round(float(old_price), 2),
        "percentage_increase": float(percentage),
        "new_price": round(float(new_price), 2),
    }


TOOL_DECLARATIONS = [
    {
        "type": "function",
        "name": "check_stock",
        "description": "Look up the current quantity of a single item in the inventory. Use this whenever the user asks whether something is in stock or how many there are.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "list_items",
        "description": "Return every item in the inventory with its quantity. Use this when the user asks what is in stock generally, or asks for a list, rather than about one specific item.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "add_item",
        "description": "Add stock to the inventory. If the item does not exist it is created; if it already exists the quantity is added to the existing total. Use this for restocking and for new deliveries.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to add. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "remove_stock",
        "description": "Reduce the quantity of an existing item. Use this when items are sold, shipped or used. This does NOT delete the item; it only lowers the number.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to remove. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "delete_item",
        "description": "Permanently remove an item and its record from the inventory entirely. This is destructive. Only use it when the user clearly wants the item gone, not when they want to reduce its quantity.",
        "parameters": {
            "type": "object",
            "properties": {

                "name": {
                    "type": "string",
                    "description": "The name of the item to delete.",
                },
            },
            "required": ["name"],
        },
    },
    
    {
        "type": "function",
        "name": "calculate_cost",
        "description": "Calculate the total cost of a specified quantity of an inventory item, including a VAT percentage. Use this when the user asks about prices, costs, totals, or VAT.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Chocolate Bar'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of units to calculate the cost for.",
                },
                "vat_percentage": {
                    "type": "number",
                    "description": "VAT percentage, e.g. 10 for 10% VAT. Use 0 if no VAT is requested.",
                },
            },
            "required": ["name", "quantity", "vat_percentage"],
        },
    },
    {
    "type": "function",
    "name": "increase_price",
    "description": "Increase the price of an existing inventory item by a percentage. Use this when the user asks to raise or increase an item's price by a certain percent.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the item, e.g. 'Chocolate Bar'.",
            },
            "percentage": {
                "type": "number",
                "description": "The percentage to increase the price by, e.g. 50 for a 50% increase.",
            },
        },
        "required": ["name", "percentage"],
    },
},

]


TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
    "calculate_cost": calculate_cost,
    "increase_price": increase_price,
}
