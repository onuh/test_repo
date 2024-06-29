/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { InvoiceControllerList } from "@daysum_technical_test/views/daysum_technical_test/daysum_technical_test_list_controller";


export const InvoiceListView = {
    ...listView,
    Controller: InvoiceControllerList,
};

registry.category("views").add("daysum_invoice_list", InvoiceListView);
