#!/usr/bin/python3
import base64
import db_manager
import uuid
import matplotlib.pyplot as plt
from io import BytesIO
import tools
import invvars

def mass_import_items(path: str):
    """
    ###Not ready for production.###
    It is used to initalize the primary db with data from a csv.
    Args:
        path (str): Path to a csv file. Must contain
    CSV File Requirements:
        Fields, must contain: A "part number" field, that is unique to each part.
            "part Name" field that is the name/desc for the part, does not need to be unique
            "quantity" field that is an integer, and is the quantity of the part.
    Raises:
        FileError: [description]
    """

    if not path.endswith(".csv"):
        raise tools.FileError("Improper File type, needs to be a csv format.")
    fhand = open(path, "r", encoding="utf-8-sig")
    fread = fhand.readlines()
    part_num_poss = ["PART_NUM", "PART_NUMBER", "PART NUM", "PART NUMBER"]
    part_name_poss = ["PART_NAME", "PART NAME", "PART_NAM"]
    qty_poss = [
        "PART_QTY",
        "PART_QUANTITY",
        "PART QTY",
        "PART QUANTITY",
        "QUANTITY",
        "QTY",
    ]
    first = True
    for i, line in enumerate(fread):
        line = line.rstrip("\n").split(",")
        print(line)
        if first:
            first = False
            fields: list = [x.upper() for x in line]
            for p in part_num_poss:
                if p in fields:
                    p_num_index = fields.index(p)
                    tools.logger(
                        1, "Dataio.mass_import_items: Found Part Number field."
                    )
                    break
            for p in part_name_poss:
                if p in fields:
                    tools.logger(
                        1, "Dataio.mass_import_items: Found Part Name field."
                    )
                    p_name_index = fields.index(p)
                    break
            for p in qty_poss:
                if p in fields:
                    tools.logger(
                        1, "Dataio.mass_import_items: Found Qty field."
                    )
                    qty_index = fields.index(p)
                    break
        else:
            if len(line) < 2:
                tools.logger(
                    1, "Dataio.mass_import_items Could not import this line."
                )
            else:
                val = {
                    "part_number": line[p_num_index],
                    "part_name": line[p_name_index],
                    "qty": line[qty_index],
                }
                items.new(val, backup=False)
                print("PartNum:", val["part_number"])
                tools.logger(1,"Dataio.mass_import_items: Created new item! With part number: " + line[p_num_index],)


class transactions:

    def status(part_uuid:str, status:str):
        trs_uuid = tool.new_uuid(True, "TRANS")
        vals = {
            "datetime": tools.now(),
            "part_number_uuid": part_uuid,
            "typ": status,
            "transaction_uuid": trs_uuid,
        }
        db = db_manager.db()
        conn = db.engine.connect()
        conn.execute(db.table["transactions"].insert(vals))
        conn.close()
        tools.logger(1, "dataio.transactions.status: Updated part_uuid: " + part_uuid + " to status: " + status)

    def verify(part_num, qty, comment=""):
        raise NotImplementedError("Not ready for use.")
        prt_uuid = items.find(part_num)["part_uuid"]
        tr_uuid = tool.new_uuid(record=True, typ="TRANS")
        vals = {
            "datetime": tools.now(),
            "part_number_uuid": prt_uuid,
            "typ": "VERIFY",
            "qty": qty,
            "dest": "",
            "source": "",
            "comment": comment,
            "transaction_uuid": tr_uuid,
        }
        db = db_manager.db()
        conn = db.engine.connect()
        conn.execute(db.table["transactions"].insert(vals)).close()

    def checkio(part_uuid:str, qty:str, io:str, dest:str="", src:str="", comment:str=""):
        if io not in ["OUT", "IN"]:
            raise tools.dbEntryError("io must be either 'IN' or 'OUT'")
        tr_uuid = tool.new_uuid(record=True, typ="TRANS")
        vals = {
            "datetime": tools.now(),
            "part_number_uuid": part_uuid,
            "typ": io,
            "qty": qty,
            "dest": dest,
            "source": src,
            "comment": comment,
            "transaction_uuid": tr_uuid,
        }
        db = db_manager.db()
        conn = db.engine.connect()
        if io == "IN":
            conn.execute(
                db.table["items"]
                .update()
                .where(db.table["items"].c.part_uuid == part_uuid)
                .values({"qty": db.table["items"].c.qty + qty})
            )
        elif io == "OUT":
            conn.execute(
                db.table["items"]
                .update()
                .where(db.table["items"].c.part_uuid == part_uuid)
                .values({"qty": db.table["items"].c.qty - qty})
            )
        conn.execute(db.table["transactions"].insert(vals))
        conn.close()
        tools.logger(1, "dataio.transaction.checkio: Updated new check in/out transaction for part: " + part_uuid + " io: " + io + " qty: " + str(qty))

    def get_transactions(types="", cnt=-1):
        """Setup to return a list of transactions.

        Args:
            starttime (str or datetime, optional): str of startime for the filter. Defaults to None.
            endtime (str or datetime, optional): endtime filter.. Defaults to None.
            types (str or list, optional): can be used to filter by types. Defaults to None.

        Returns:
            tuple[fields, results]: Fields and records from transactions.
        """
        db: db_manager.db = db_manager.db()
        conn = db.engine.connect()
        if types == "" and cnt == -1:
            result = conn.execute(db.table["transactions"].select()).all()
        elif cnt == -1 and type(types) == list:
            result = conn.execute(
                db.table["transactions"]
                .select()
                .where(db.table["transactions"].c.typ in types)
            ).all()
        elif cnt == -1 and type(types) == str:
            result = conn.execute(
                db.table["transactions"]
                .select()
                .where(db.table["transactions"].c.typ == types)
            ).all()
        elif types == None and cnt != -1:
            result = conn.execute(db.table["transactions"].select()).all()
        elif cnt != -1 and type(types) == list:
            result = conn.execute(
                db.table["transactions"]
                .select()
                .where(db.table["transactions"].c.typ in types)
            ).all()
        elif cnt != -1 and type(types) == str:
            result = conn.execute(
                db.table["transactions"]
                .select()
                .where(db.table["transactions"].c.typ == types)
            ).all()
        conn.close()
        fields = [x.name for x in db.table["transactions"].columns]
        tools.logger(1, "dataio.transactions.get_transactions: Retrieved " + str(len(result)) + " transactional records.")
        return (fields, result)

    def item_transactions(part_number="", part_uuid=""):
        if part_uuid == "":
            part_uuid = items.find(part_number)["part_uuid"]
        db = db_manager.db()
        conn = db.engine.connect()
        result = conn.execute(
            db.table["transactions"]
            .select()
            .where(db.table["transactions"].c.part_number_uuid == part_uuid)
        ).all()
        conn.close()
        fields = [x.name for x in db.table["transactions"].columns]
        tools.logger(1, "dataio.transactions.get_transactions: Retrieved " + str(len(result)) + " transactional records for part_uuid: " + part_uuid +  " .")
        return (fields, result)


class items:
    def status(part_uuid: str, status):
        if status not in ["INUSE", "ARCHIVED"]:
            raise tools.dbEntryError("Cannot utilize listed status.")
        transactions.status(part_uuid, status)
        db = db_manager.db()
        db.engine.connect().execute(
            db.table["items"]
            .update()
            .where(db.table["items"].c.part_uuid == part_uuid)
            .values({"status": status})
        ).close()
        tools.logger(1, "dataio.items.status: Chaning part status for part_uuid: " + part_uuid + " to status: " + status)

    def num_check(prt_num):
        raise NotImplementedError("Needs migration into new uuid use system...")
        """Checks if a part number already exsists in the items.part_number field.

        Args:
            prt_num (str): Part number to be checked. IS CASE SENSITIVE!
        Return:
            bool: True means it already is in the db.
        """
        db = db_manager.db()
        conn = db.engine.connect()
        res = conn.execute(
            db.table["items"].select().where(db.table["items"].c.part_number == prt_num)
        ).all()
        conn.close()
        tools.logger(
            1,
            "Dataio.part_num_check: Found " + str(len(res)) + " part numbers in db.",
        )
        tools.logger(
            1,
            "Dataio.part_num_check: Status of part number entered: "
            + prt_num
            + " in db",
        )
        return len(res) == 1

    def new(item: dict, verify_part_num: bool = True, backup=True):
        """Creates a new item in the items database table.
        Supports logging
        Args:
            item: dict: should be the dictionary matching the table structure.
            This dictionary this should match the user defined columns from the data_struc.json
        Raises:
            ItemError: raised if the part already exsits the in the db.
        """
        if verify_part_num:
            item["part_number"] = tool.verify_part_num(item["part_number"])
        tools.logger(
            1,
            "DataIO.new_item: Creating new item with part number: '"
            + item["part_number"]
            + "'",
        )
        if items.num_check(item["part_number"]):
            tools.logger(1, "dataio.item.new: Already found part number in db.")
            # raise ItemError("Item Already Exsists in the db.")
        new_id = tool.new_uuid(record=True, typ="PART")
        item["part_uuid"] = new_id
        item["status"] = "INUSE"
        db = db_manager.db()
        if backup:
            db.backup()
        conn = db.engine.connect()
        conn.execute(db.table["items"].insert(values=item))
        conn.execute(db.table["uuids"].insert(values={"uuid": new_id, "typ": "item"}))
        conn.close()
        tools.logger(1, "DataIO.new_item: Added new item to db.items.")

    def find(part_num: str = None, part_uuid: str = None):
        """Find a part_num in db.items and returns it.
        Returns all fields in db.items
        Args:
            part_num (str): Part number to be found.

        Returns:
            dict: column name and data
        """
        db = db_manager.db()
        conn = db.engine.connect()
        if part_num != None:
            res = conn.execute(
                db.table["items"]
                .select()
                .where(db.table["items"].c.part_number == part_num)
            ).all()[0]
            tools.logger(1,"Dataio.find: Found " + str(len(res)) + " where items.part_number ='" + part_num + "'.")
        elif part_uuid != None:
            res = conn.execute(
                db.table["items"]
                .select()
                .where(db.table["items"].c.part_uuid == part_uuid)
            ).all()[0]
            tools.logger(
                1,
                "Dataio.find: Found "
                + str(len(res))
                + "where items.part_number ='"
                + part_uuid
                + "'.",
            )
        conn.close()
        fields = [x.name for x in db.table["items"].columns]
        return {fields[i]: res[i] for i in range(0, len(fields))}

    def get_all(status: str = "INUSE", limit=None):
        """Only takes status, which is either "INUSE" or "ARCHIVED"
        Returns:
            tuple(fields, results): Returns the fields and a list and results as list[tuples].
        """
        tools.logger(1, "Dataio.get_all_items: Retrieving Primary Stock Table.")
        db = db_manager.db()
        conn = db.engine.connect()
        if limit != None:
            res = conn.execute(
                db.table["items"].select().where(db.table["items"].c.status == status)
            ).all()
        else:
            res = conn.execute(
                db.table["items"].select().where(db.table["items"].c.status == status)
            ).all()
        conn.close()
        fields = [x.name for x in db.table["items"].columns]
        tools.logger(
            1, "Dataio.get_all_items: Returned " + str(len(res)) + " results."
        )
        return (fields, res)

    def edit(item: dict):
        """Edits parts in db.items. MUST have part_uuid otherwise it will not work.

        Args:
            item (dict): all keys must comply with the items.columns.
        """
        print(item)
        if "part_uuid" not in item.keys():
            raise tools.dbEntryError(
                "Must include part uuid, otherwise cannot edit part."
            )
        db = db_manager.db()
        db.backup()
        conn = db.engine.connect()
        conn.execute(
            db.table["items"]
            .update()
            .where(db.table["items"].c.part_uuid == item["part_uuid"])
            .values(item)
        ).close()

    def gen_tags():
        db = db_manager.db()
        conn = db.engine.connect()
        conn.execute(
            db.table["items"]
            .update()
            .values(
                {
                    db.table["items"].c.tags: db.table["items"].c.part_number
                    + db.table["items"].c.part_name
                }
            )
        )

    def transactions_hist(part_uuid):
        fields, res = transactions.item_transactions(part_uuid=part_uuid)
        nqty = []
        ndts = []
        for r in res:
            x = r[fields.index("qty")]
            if x == None:
                continue

            if r[fields.index("typ")] == "OUT":
                ndts.append(r[fields.index("datetime")])
                nqty.append(-x)
            elif r[fields.index("typ")] == "IN":
                ndts.append(r[fields.index("datetime")])
                nqty.append(x)
            elif x[fields.index("typ")] == "VERIFY":
                continue
        if len(nqty) != 0:
            maxqty = max(nqty) + 2
            minqty = min(nqty) - 1
            maxdts = max(ndts) + 1
            mindts = min(ndts) - 1
        else:
            return ""
        tmpfile = BytesIO()
        fig, ax = plt.subplots()
        ax.plot(ndts, nqty, "ro")
        ax.set_xticks = [x for x in range(minqty-1, maxqty+1)]
        plt.ylabel("QTY Change")
        plt.xlabel("Datetime Stamp")
        plt.savefig(tmpfile, format="png")
        encoded = base64.b64encode(tmpfile.getvalue()).decode("utf8")
        return encoded


class users:
    def new(usr):
        """Needs username, firstname, lastname, uuid, level.

        Args:
            usr (dict): [description]
        """
        usr["user_uuid"] = tool.new_uuid(True, "USER")
        db = db_manager.db()
        conn = db.engine.connect()
        conn.execute(db.table["users"].insert(usr)).close()

    def get_all():
        db = db_manager.db()
        conn = db.engine.connect()
        res = conn.execute(db.table["users"].select()).all()
        conn.close()
        fields = [x.name for x in db.table["users"].columns]
        return (fields, res)


class tool:
    def new_uuid(record=False, typ=""):
        while True:
            ret = str(uuid.uuid4())
            db = db_manager.db()
            conn = db.engine.connect()
            sqlr = conn.execute(
                db.table["uuids"].select().where(db.table["uuids"].c.uuid == ret)
            ).all()
            if len(sqlr) < 1:
                conn.execute(db.table["uuids"].insert({"uuid": ret, "typ": typ}))
                conn.close()
                return ret

    def verify_part_num(part_num: str):
        return part_num.upper()


if __name__ == "__main__":
    invvars.init()
    tools.load_config()
