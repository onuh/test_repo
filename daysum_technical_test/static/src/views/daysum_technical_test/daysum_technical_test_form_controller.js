/** @odoo-module **/

import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { FormController } from "@web/views/form/form_controller";



export class InvoiceController extends FormController {
    setup() {
        super.setup();
        
    }
    
    /**
     * @override
     */


    getActionMenuItems() {

        const otherActionItems = [];
        

        if (this.archInfo.activeActions.create && this.archInfo.activeActions.duplicate) {
            otherActionItems.push({
                key: "duplicate",
                description: this.env._t("Duplicate"),
                callback: () => this.duplicateRecord(),
            });
        }
        // this condition is modified for only entries not posted
        if (this.archInfo.activeActions.delete && !this.model.root.isVirtual && this.model.root.data.state != 'posted') {
            otherActionItems.push({
                key: "delete",
                description: this.env._t("Delete"),
                callback: () => this.deleteRecord(),
                skipSave: true,
            });
        }
        return Object.assign({}, this.props.info.actionMenus, { other: otherActionItems });
    }

  
}