from openerp.addons.account.tests.account_test_users import AccountTestUsers
import datetime


class TestAccountCustomerInvoice(AccountTestUsers):

    def test_customer_invoice(self):
        # Create a customer invoice
        self.account_invoice_obj = self.env['account.invoice']
        self.payment_term = self.env.ref('account.account_payment_term_advance')
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.partner3 = self.env.ref('base.res_partner_3')
        account_user_type = self.env.ref('account.data_account_type_receivable')
        self.ova = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_current_assets').id)], limit=1)

        #only adviser can create an account
        self.account_rec1_id = self.account_model.sudo(
            self.account_manager.id).create(
                dict(
                    code="cust_acc",
                    name="customer account",
                    user_type_id=account_user_type.id,
                    reconcile=True,)
        )

        invoice_line_data = [
            (0, 0,
                {
                    'product_id': self.env.ref('product.product_product_5').id,
                    'quantity': 10.0,
                    'account_id': self.env['account.account'].search(
                        [('user_type_id', '=', self.env.ref(
                            'account.data_account_type_revenue').id)],
                        limit=1).id,
                    'name': 'product test 5',
                    'price_unit': 100.00,
                    'origin': 'aaa',
                }
             ),
            (0, 0,
             {
                 'product_id': self.env.ref('product.product_product_1').id,
                 'quantity': 5.0,
                 'account_id': self.env['account.account'].search(
                     [('user_type_id', '=', self.env.ref(
                         'account.data_account_type_revenue').id)],
                     limit=1).id,
                 'name': 'product test 1',
                 'price_unit': 100.00,
                 'origin': 'aaa',
             }
             ),
            (0, 0,
             {
                 'product_id': self.env.ref('product.product_product_5').id,
                 'quantity': 10.0,
                 'account_id': self.env['account.account'].search(
                     [('user_type_id', '=', self.env.ref(
                         'account.data_account_type_revenue').id)],
                     limit=1).id,
                 'name': 'product test 5',
                 'price_unit': 100.00,
                 'origin': 'bbb',
             }
             ),
            (0, 0,
             {
                 'product_id': self.env.ref('product.product_product_5').id,
                 'quantity': 10.0,
                 'account_id': self.env['account.account'].search(
                     [('user_type_id', '=', self.env.ref(
                         'account.data_account_type_revenue').id)],
                     limit=1).id,
                 'name': 'product test 5',
                 'price_unit': 100.00,
                 'origin': 'ccc',
             }
             )
        ]

        self.account_invoice_customer0 = self.account_invoice_obj.sudo(
            self.account_user.id).create(dict(
                name="Test Customer Invoice",
                reference_type="none",
                payment_term_id=self.payment_term.id,
                journal_id=self.journalrec.id,
                partner_id=self.partner3.id,
                account_id=self.account_rec1_id.id,
                invoice_line_ids=invoice_line_data)
        )

        # I check that Initially customer invoice is in the "Draft" state
        self.assertEquals(self.account_invoice_customer0.state, 'draft')

        # I validate invoice by creating on
        self.account_invoice_customer0.signal_workflow('invoice_open')

        # I check that the invoice state is "Open"
        self.assertEquals(self.account_invoice_customer0.state, 'open')

        # I check that now there is a move attached to the invoice
        assert self.account_invoice_obj.grouped_lines_by_origin(
            self.account_invoice_customer0.id) == [
            {'origin': u'aaa', 'lines': [
                self.account_invoice_customer0.invoice_line_ids[0],
                self.account_invoice_customer0.invoice_line_ids[1]]},
            {'origin': u'bbb', 'lines': [
                self.account_invoice_customer0.invoice_line_ids[2]]},
            {'origin': u'ccc', 'lines': [
                self.account_invoice_customer0.invoice_line_ids[3]]}
        ], "group invoice by origin failed!"

