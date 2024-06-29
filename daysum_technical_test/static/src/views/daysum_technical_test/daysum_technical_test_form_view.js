/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { InvoiceController } from "@daysum_technical_test/views/daysum_technical_test/daysum_technical_test_form_controller";


export const InvoiceFormView = {
    ...formView,
    Controller: InvoiceController,
};

registry.category("views").add("daysum_invoice_form", InvoiceFormView);
