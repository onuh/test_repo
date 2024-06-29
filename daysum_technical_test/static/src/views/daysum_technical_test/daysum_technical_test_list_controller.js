/** @odoo-module **/

import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { ListController } from "@web/views/list/list_controller";


export class InvoiceControllerList extends ListController {
    setup() {
        super.setup();
        
    }
    
    /**
     * @override
     */


    getActionMenuItems() {

        const isM2MGrouped = this.model.root.isM2MGrouped;

        const otherActionItems = [];
        if (this.isExportEnable) {
            otherActionItems.push({
                key: "export",
                description: this.env._t("Export"),
                callback: () => this.onExportData(),
            });
        }

    
        // this condition is modified for only entries not posted
        if (this.activeActions.delete && !isM2MGrouped && this.model.root.selection[0].data.state != 'posted') {
            otherActionItems.push({
                key: "delete",
                description: this.env._t("Delete"),
                callback: () => this.onDeleteSelectedRecords(),
            });
        }
        const Selected = this.model.root.selection
        for(var i=0; i <= Selected.length - 1; i++){
            if(Selected[i].data.state == 'posted'){
                otherActionItems.splice(0, otherActionItems.length)
                break;
            }
        }
        return Object.assign({}, this.props.info.actionMenus, { other: otherActionItems });
    }

  
}