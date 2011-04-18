import xml.dom.minidom as dom

def get_slice_cred(fname):
    f = open(fname, 'r')
    return f.read()

def make_credential_metadata(cred, metadata_id, metadata_idref):
    return """
  <nmwg:metadata id="%s">
    <nmwg:subject metadataIdRef="%s">
%s
    </nmwg:subject>
    <nmwg:eventType>http://perfsonar.net/ns/protogeni/auth/credential/1</nmwg:eventType>
  </nmwg:metadata>
""" % (metadata_id, metadata_idref, cred) 

def make_UNIS_request(type="TSQueryRequest", data_content="", cred=None):
    metadata_id = 'meta0'
    cred_metadata = ""
    if cred:
        cred_metadata = make_credential_metadata(cred, 'cred0', metadata_id)
        metadata_id = 'cred0'

    msg="""
<nmwg:message type="%s" xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/">
  <nmwg:metadata id="meta0">
    <nmwg:eventType>http://ggf.org/ns/nmwg/topology/20070809</nmwg:eventType>
  </nmwg:metadata>
%s
  <nmwg:data id="data0" metadataIdRef="%s">
%s
  </nmwg:data>
</nmwg:message>
"""
    return msg % (type, cred_metadata, metadata_id, data_content)    
    
def make_UNISQueryAll_message(cred=None):
    return make_UNIS_request(type="TSQueryRequest", cred=cred)

def make_UNISAdd_message(topology, cred=None):
    return make_UNIS_request(type="TSAddRequest", data_content=topology, cred=cred)

def make_UNISReplace_message(topology, cred=None):
    return make_UNIS_request(type="TSReplaceRequest", data_content=topology, 
                                    cred=cred)


def create_urn(domain, node=None, port=None, link=None, service=None):
    """
    Create UNIS URN.
    
    Example if domain is udel.edu then the URN is
    'urn:ogf:network:domain=udel.edu'
    And if domain is udel.edu and node is stout then the URN is
    'urn:ogf:network:domain=udel.edu:node=stout'
    """
    assert domain, "URN must be fully qualified; no domain provided"
    urn = "urn:ogf:network:domain=%s" % domain
    
    if node != None:
        urn = urn + ":node=%s" % node
       
    if port != None:
        assert node != None, "URN must be fully qualified; no node given for port"
        urn = urn + ":port=%s" % port
   
    if link != None:
        assert node == None, "URN must be fully qualified; invalid link urn"
        urn = urn + ":link=%s" % link
    
    if service != None:
        assert node != None and port == None, "URN must be fully qualified; invalid service urn"
        urn = urn + ":service=%s" % service
    
    return urn


# As bizarre as it sounds, (mini)DOM doesn't provide a 
# getElementsByTag that gets from only the immediate children.
def get_qualified_xml_children(element, ns, name):
    elements = []
    for child in element.childNodes:
        if isinstance(child, dom.Element):
            if child.namespaceURI == ns and child.localName == name:
                elements.append(child)
    return elements

def get_unique_xml_child(element, ns, name):
    # XXX: Maybe namespace could be None?
    assert element != None and ns != None and name != None
    
    children = get_qualified_xml_children(element, ns, name)
    if len(children) > 1:
        raise Exception, element.localName + ": has more than one " + \
                         name + " element!"
    
    if len(children) == 1:
        return children[0]
    return None

def create_text_element(dom, ns, name, data, attributes=()):
    if ns:
        e = dom.createElementNS(ns, name)
    else:
        e = dom.createElement(name)
    
    e.appendChild(dom.createTextNode(data))
    
    for (attr_name, attr_value) in attributes:
        e.setAttribute(attr_name, attr_value)
        
    return e

def clone_children(node_from, node_to, ignore_list=()):
    for child in node_from.childNodes:
        if (child.namespaceURI, child.localName) in ignore_list:
            continue
        node_to.appendChild( child.cloneNode(True) )
