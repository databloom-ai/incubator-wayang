/*
 *
 *  * Licensed to the Apache Software Foundation (ASF) under one
 *  * or more contributor license agreements.  See the NOTICE file
 *  * distributed with this work for additional information
 *  * regarding copyright ownership.  The ASF licenses this file
 *  * to you under the Apache License, Version 2.0 (the
 *  * "License"); you may not use this file except in compliance
 *  * with the License.  You may obtain a copy of the License at
 *  *
 *  *     http://www.apache.org/licenses/LICENSE-2.0
 *  *
 *  * Unless required by applicable law or agreed to in writing, software
 *  * distributed under the License is distributed on an "AS IS" BASIS,
 *  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  * See the License for the specific language governing permissions and
 *  * limitations under the License.
 *
 */

package org.apache.wayang.api.sql.calcite.converter;

import org.apache.calcite.rel.RelNode;
import org.apache.wayang.api.sql.calcite.rel.WayangFilter;
import org.apache.wayang.api.sql.calcite.rel.WayangProject;
import org.apache.wayang.api.sql.calcite.rel.WayangTableScan;
import org.apache.wayang.core.plan.wayangplan.Operator;

public class WayangRelConverter {

    public Operator convert(RelNode node) {
        if(node instanceof WayangTableScan) {
            return new WayangTableScanVisitor(this).visit((WayangTableScan)node);
        } else if (node instanceof WayangProject) {
            return new WayangProjectVisitor(this).visit((WayangProject) node);
        } else if (node instanceof WayangFilter) {
            return new WayangFilterVisitor(this).visit((WayangFilter) node);
        }
        throw new IllegalStateException("Operator translation not supported yet");
    }


}
